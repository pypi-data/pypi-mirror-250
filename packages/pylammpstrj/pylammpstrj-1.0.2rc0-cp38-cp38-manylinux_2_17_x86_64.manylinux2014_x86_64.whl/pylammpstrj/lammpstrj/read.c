/**
 * \file
 * Implementation of the reading functions.
 *
 * The API currently implements two versions of the reading function: a serial,
 * and a parallel one.
 */
#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "utils.h"

static void read_current_step(FILE *input, unsigned long *current_step)
{
    char dump[READ_BUFFER_LIMIT];
    long pos = ftell(input);
    while (fscanf(input, "ITEM: TIMESTEP %lu", current_step) != 1)
        if (fgets(dump, READ_BUFFER_LIMIT, input) == NULL)
        {
            errno = EIO;
            perror("Error while skipping a line (read_current_step)");
            return;
        }
    fseek(input, pos, SEEK_SET);
}

/** Replaces all new line characters in `str` by `chr`.
 *
 */
static void string_remove_new_lines(char *str, char chr)
{
    for (int c = strlen(str) - 1; 0 <= c; c--)
        if (str[c] == '\0')
            continue;
        else if (str[c] == '\n')
            str[c] = chr;
}

#define DUMP_FORMAT_OFFSET 12

static void read_dump_format(FILE *input, char dump_format[READ_BUFFER_LIMIT])
{
    char line[READ_BUFFER_LIMIT];

    long pos = ftell(input);
    do
        if (fgets(line, READ_BUFFER_LIMIT, input) == NULL)
        {
            errno = EIO;
            perror("Error while skipping a line (read_dump_format)");
            return;
        }
    while (strncmp(line, "ITEM: ATOMS", DUMP_FORMAT_OFFSET - 1) != 0);

    strncpy(dump_format, line + DUMP_FORMAT_OFFSET, READ_BUFFER_LIMIT);
    string_remove_new_lines(dump_format, '\0');
    fseek(input, pos, SEEK_SET);
}

#define BASE_N_CONFIGURATIONS 100
#define N_CONFIGURATIONS_INCR 100

void trajectory_read(const char *file_name, const unsigned long start,
                     char user_format[READ_BUFFER_LIMIT],
                     struct Trajectory *trajectory)
{
    // Opening the file
    FILE *input = fopen(file_name, "r");
    if (input == NULL)  // File could not be open
    {
        errno = EIO;
        perror("Error while opening the file (trajectory_read)");
        return;
    }

    // Skipping the first configurations
    trajectory_skip(&input, start);
    if (errno != 0)  // Something went wrong
    {
        fclose(input);
        return;
    }

    // Getting the current step
    unsigned long current_step;
    read_current_step(input, &current_step);
    if (errno != 0)  // Something went wrong
    {
        fclose(input);
        return;
    }

    // Getting the dump format
    char dump_format[READ_BUFFER_LIMIT];
    if (user_format[0] == '\0')
        read_dump_format(input, dump_format);
    else
    {
        strncpy(dump_format, user_format, READ_BUFFER_LIMIT);
        string_remove_new_lines(dump_format, '\0');
    }

    // Initializing the atom builder
    struct AtomBuilder atom_builder = atom_builder_new(dump_format, input);
    if (errno != 0)  // Something went wrong
    {
        fclose(input);
        return;
    }

    // Preparing the arrays
    unsigned int *N_atoms =
        malloc(BASE_N_CONFIGURATIONS * sizeof(unsigned int));
    if (N_atoms == NULL)  // Allocation failed
    {
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_read.N_atoms)");
        atom_builder_delete(&atom_builder);
        fclose(input);
        return;
    }
    unsigned int *steps = malloc(BASE_N_CONFIGURATIONS * sizeof(unsigned int));
    if (steps == NULL)
    {
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_read.steps)");
        free(N_atoms);
        atom_builder_delete(&atom_builder);
        fclose(input);
        return;
    }
    struct Box *boxes = malloc(BASE_N_CONFIGURATIONS * sizeof(struct Box));
    if (boxes == NULL)  // Allocation failed
    {
        errno = ENOMEM;
        perror("Error while allocating memory (trajectory_read.boxes)");
        free(steps);
        free(N_atoms);
        atom_builder_delete(&atom_builder);
        fclose(input);
        return;
    }
    unsigned long boxes_size = BASE_N_CONFIGURATIONS;
    struct Atom *atoms = NULL;
    unsigned long atoms_size = 0;

    // Preparing the variables
    char line[READ_BUFFER_LIMIT];
    unsigned long step;
    char box_flag[BOX_FLAG_LIMIT] = {0};
    double box_bounds[BOX_BOUNDS_LIMIT] = {0};
    unsigned int n_atoms;
    char format[READ_BUFFER_LIMIT];

    unsigned long N_configurations = 0;
    unsigned long total_atoms = 0;  // To keep track of the number of atoms read

    // Reading
    int chr = fgetc(input);
    while (chr != EOF)
    {
        ungetc(chr, input);

        // Reading the timestep and number of atoms
        if (fscanf(input,
                   "ITEM: TIMESTEP %lu"
                   " ITEM: NUMBER OF ATOMS %u",
                   &step, &n_atoms) != 2)  // Error while scanning
        {
            errno = EINVAL;
            perror(
                "Error while scanning a line "
                "(trajectory_read.timestep/n_atoms)");
            for (unsigned int a = 0; a < total_atoms; a++)
                atom_delete(atoms + a);
            if (atoms != NULL) free(atoms);
            free(boxes);
            free(steps);
            free(N_atoms);
            atom_builder_delete(&atom_builder);
            fclose(input);
            return;
        }

        // Reading the box bounds
        if (fscanf(input, " ITEM: BOX BOUNDS %" BOX_FLAG_SCANF_LIMIT "c",
                   box_flag) != 1)  // Error while scanning
        {
            errno = EINVAL;
            perror("Error while scanning a line (trajectory_read.box_flag)");
            for (unsigned int a = 0; a < total_atoms; a++)
                atom_delete(atoms + a);
            if (atoms != NULL) free(atoms);
            free(boxes);
            free(steps);
            free(N_atoms);
            atom_builder_delete(&atom_builder);
            fclose(input);
            return;
        }

        for (unsigned int b = 0; b < BOX_BOUNDS_LIMIT; b++)
            if (fscanf(input, "%lf ", &(box_bounds[b])) !=
                1)  // Error while scanning
            {
                errno = EINVAL;
                perror(
                    "Error while scanning a line (trajectory_read.box_bounds)");
                for (unsigned int a = 0; a < total_atoms; a++)
                    atom_delete(atoms + a);
                if (atoms != NULL) free(atoms);
                free(boxes);
                free(steps);
                free(N_atoms);
                atom_builder_delete(&atom_builder);
                fclose(input);
                return;
            }

        // Checking the dump format
        if (fgets(format, READ_BUFFER_LIMIT, input) ==
            NULL)  // Something went wrong
        {
            errno = EIO;
            perror("Error while reading a line (trajectory_read.format)");
            for (unsigned int a = 0; a < total_atoms; a++)
                atom_delete(atoms + a);
            if (atoms != NULL) free(atoms);
            free(boxes);
            free(steps);
            free(N_atoms);
            atom_builder_delete(&atom_builder);
            fclose(input);
            return;
        }
        string_remove_new_lines(format, '\0');
        if (strncmp(format + DUMP_FORMAT_OFFSET, dump_format,
                    READ_BUFFER_LIMIT) != 0)  // The dump formats are different
        {
            errno = EINVAL;
            perror(
                "Error while comparing strings (trajectory_read.dump_format)");
            for (unsigned int a = 0; a < total_atoms; a++)
                atom_delete(atoms + a);
            if (atoms != NULL) free(atoms);
            free(boxes);
            free(steps);
            free(N_atoms);
            atom_builder_delete(&atom_builder);
            fclose(input);
            return;
        }

        // Reallocating memory
        if (N_configurations == boxes_size)
        {
            unsigned int *new_N_atoms =
                realloc(N_atoms, (boxes_size + N_CONFIGURATIONS_INCR) *
                                     sizeof(unsigned int));
            if (new_N_atoms == NULL)  // Could not realloc memory
            {
                errno = ENOMEM;
                perror(
                    "Error while reallocating memory (trajectory_read.boxes)");
                for (unsigned int a = 0; a < total_atoms; a++)
                    atom_delete(atoms + a);
                if (atoms != NULL) free(atoms);
                free(boxes);
                free(steps);
                free(N_atoms);
                atom_builder_delete(&atom_builder);
                fclose(input);
                return;
            }
            N_atoms = new_N_atoms;

            unsigned int *new_steps =
                realloc(steps, (boxes_size + N_CONFIGURATIONS_INCR) *
                                   sizeof(unsigned int));
            if (new_steps == NULL)  // Could not realloc memory
            {
                errno = ENOMEM;
                perror(
                    "Error while reallocating memory (trajectory_read.boxes)");
                for (unsigned int a = 0; a < total_atoms; a++)
                    atom_delete(atoms + a);
                if (atoms != NULL) free(atoms);
                free(boxes);
                free(steps);
                free(N_atoms);
                atom_builder_delete(&atom_builder);
                fclose(input);
                return;
            }
            steps = new_steps;

            struct Box *new_boxes =
                realloc(boxes, (boxes_size + N_CONFIGURATIONS_INCR) *
                                   sizeof(struct Box));
            if (new_boxes == NULL)  // Could not realloc memory
            {
                errno = ENOMEM;
                perror(
                    "Error while reallocating memory (trajectory_read.boxes)");
                for (unsigned int a = 0; a < total_atoms; a++)
                    atom_delete(atoms + a);
                if (atoms != NULL) free(atoms);
                free(boxes);
                free(steps);
                free(N_atoms);
                atom_builder_delete(&atom_builder);
                fclose(input);
                return;
            }
            boxes = new_boxes;

            boxes_size += N_CONFIGURATIONS_INCR;
        }

        // Saving the number of atoms
        N_atoms[N_configurations] = n_atoms;

        // Saving the timestep
        steps[N_configurations] = step;

        // Saving the box
        boxes[N_configurations] = box_new(box_flag, box_bounds);

        // Reallocating memory
        {
            struct Atom *new_atoms =
                realloc(atoms, (atoms_size + N_atoms[N_configurations]) *
                                   sizeof(struct Atom));
            if (new_atoms == NULL)
            {
                errno = ENOMEM;
                perror(
                    "Error while reallocating memory (trajectory_read.atoms)");
                for (unsigned int a = 0; a < total_atoms; a++)
                    atom_delete(atoms + a);
                if (atoms != NULL) free(atoms);
                free(N_atoms);
                free(steps);
                free(boxes);
                atom_builder_delete(&atom_builder);
                fclose(input);
                return;
            }
            atoms = new_atoms;
            atoms_size += N_atoms[N_configurations];
        }

        // Reading the atoms
        for (unsigned int a = 0; a < N_atoms[N_configurations]; a++)
        {
            if (fgets(line, READ_BUFFER_LIMIT, input) ==
                NULL)  // Something went wrong
            {
                errno = EIO;
                perror("Error while reading a line (trajectory_read.line)");
                for (unsigned int a = 0; a < total_atoms; a++)
                    atom_delete(atoms + a);
                if (atoms != NULL) free(atoms);
                free(boxes);
                free(steps);
                free(N_atoms);
                atom_builder_delete(&atom_builder);
                fclose(input);
                return;
            }
            atoms[total_atoms + a] = read_atom_entry(atom_builder, line);
            if (errno != 0)  // Could not read the atom entry
            {
                for (unsigned int at = 0; at <= total_atoms + a; at++)
                    atom_delete(atoms + at);
                if (atoms != NULL) free(atoms);
                free(boxes);
                free(steps);
                free(N_atoms);
                atom_builder_delete(&atom_builder);
                fclose(input);
                return;
            }
        }
        total_atoms += N_atoms[N_configurations];

        N_configurations++;
        chr = fgetc(input);
    }

    fclose(input);
    trajectory_init(trajectory, atom_builder, N_configurations, steps, N_atoms,
                    boxes, atoms);
}
