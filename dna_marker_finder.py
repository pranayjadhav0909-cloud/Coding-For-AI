# Task 1: search4letters

def search4letters(phrase: str, letters: str = 'ATCG') -> set:
    """Return the set of target letters found in phrase."""
    return set(letters).intersection(set(phrase))


# Task 2: mutation vs reassignment

def analyze_sequence(sequence_list, marker):
    """Appends marker to sequence_list in place (mutates shared object)."""
    print(f"Inside (Start) - ID: {id(sequence_list)} | Data: {sequence_list}")
    sequence_list.append(marker)
    print(f"Inside (End)   - ID: {id(sequence_list)} | Data: {sequence_list}")


def analyze_sequence_rebind(sequence_list, marker):
    """Rebinds local name instead of mutating (bonus experiment)."""
    print(f"Inside (Start) - ID: {id(sequence_list)}")
    sequence_list = sequence_list + [marker]  # new object, local rebind only
    print(f"Inside (End)   - ID: {id(sequence_list)} | Data: {sequence_list}")


def main():
    # --- Task 1: positional, keyword, default ---
    print(search4letters('TGGACC', 'GC'))
    print(search4letters(letters='CG', phrase='TGGACC'))
    print(search4letters('TGGACC'))

    # --- Task 2.1: mutation demo ---
    dna_database = ['AATCCG', 'TGGCTA']
    print(f"Before - ID: {id(dna_database)} | Data: {dna_database}")
    analyze_sequence(dna_database, 'CGAT')
    print(f"After  - ID: {id(dna_database)} | Data: {dna_database}")

    # --- Task 2.3: slice experiment (shallow copy breaks the link) ---
    dna_database = ['AATCCG', 'TGGCTA']
    print(f"Before - ID: {id(dna_database)} | Data: {dna_database}")
    analyze_sequence(dna_database[:], 'CGAT')
    print(f"After  - ID: {id(dna_database)} | Data: {dna_database}")

    # --- Task 2.4: bonus - rebind instead of mutate ---
    dna_database = ['AATCCG', 'TGGCTA']
    analyze_sequence_rebind(dna_database, 'CGAT')
    print(f"After  - ID: {id(dna_database)} | Data: {dna_database}")

    # --- Edge cases ---
    print(search4letters(''))                       # empty set, no error
    print(search4letters('TGGACC', letters='GC'))    # mixed args, same result

    dna_database = ['AATCCG', 'TGGCTA']
    for i in range(3):
        analyze_sequence(dna_database[:], f'MARK{i}')  # each call isolated
    print(dna_database)  # unchanged


if __name__ == "__main__":
    main()
