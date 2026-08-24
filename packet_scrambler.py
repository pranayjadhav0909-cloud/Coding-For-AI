"""
Data Rotation Engine - Packet Scrambler
Problem Set 3: List Manipulation, Slicing, and Multi-Assignment Unpacking

This script implements a four-stage pipeline that takes a list-based data
packet through a structural rotation (Stage 2), an in-place correction
pass (Stage 3), and a final integrity check (Stage 4), without relying on
any external library. Stage 1 performs basic validation on the input.

The four stages are:
    1. Input Validation and Test Data  - confirm the packet is non-empty
       and at least 10 elements long using short-circuit logic.
    2. The "Middle-Out" Swap           - slice the packet into two halves
       and rebuild a new list with the reversed back half in front.
    3. In-Place Correction             - insert a "SYNC-BIT" marker next
       to the middle element (if it is an int) and strip out every 0.
    4. Memory Integrity Check          - print the original and final
       packets side by side and unpack the final packet's header/footer.

Author: Pranay Jadhav
Course: Coding for AI 
Date: 21 August 2026
"""


def main():

    # Stage 1: Input Validation and Test Data
    packet = [5, 12, 0, 8, 21, 34, 7, 19, 0, 3]

    print("--- Stage 1: Input Validation ---")
    if packet and len(packet) >= 10:
        print("Validation passed. Processing packet...")
    else:
        print("Validation failed: packet is empty or too short.")
    print(f"Original packet: {packet}\n")


    # Stage 2: The "Middle-Out" Swap
    midpoint = len(packet) // 2
    front_half = packet[:midpoint]
    back_half = packet[midpoint:]
    scrambled = back_half[::-1] + front_half

    print("--- Stage 2: Middle-Out Swap ---")
    print(f"Front half : {front_half}")
    print(f"Back half  : {back_half}")
    print(f"Scrambled  : {scrambled}")
    print(f"id(packet) == id(front_half): {id(packet) == id(front_half)}  # Expect: False")
    print(f"Original packet still: {packet}\n")

    # Stage 3: In-Place Correction
    print("--- Stage 3: In-Place Correction ---")
    middle_index = len(scrambled) // 2
    if type(scrambled[middle_index]) is int:
        scrambled.insert(middle_index + 1, "SYNC-BIT")
        print(f"Sync-bit inserted after index {middle_index}: {scrambled}")
    else:
        print(
            f"Value at middle index {middle_index} is not an integer; "
            "skipping Sync-Bit insertion."
        )

    while 0 in scrambled:
        scrambled.remove(0)
    print(f"After zero removal: {scrambled}\n")

    # Stage 4: Memory Integrity Check
    print("--- Stage 4: Memory Integrity Check ---")
    print(f"Original packet : {packet}")
    print(f"Final scrambled : {scrambled}")

    first, *middle, last = scrambled
    print(f"Header: {first} Footer: {last} Body length: {len(middle)}")

    unchanged = packet == [5, 12, 0, 8, 21, 34, 7, 19, 0, 3]
    print(f"\nOriginal packet unchanged: {unchanged}")


def scramble(packet):
    """Stretch goal: package the four-stage pipeline into a reusable function.

    Runs the same rotation, correction, and integrity logic as main(), but
    returns the final scrambled list instead of printing it. Handles the
    edge cases from Section 6: odd-length packets, a non-integer value at
    the middle index, and packets that contain no zeros at all.
    """
    if not packet:
        return []

    midpoint = len(packet) // 2
    front_half = packet[:midpoint]
    back_half = packet[midpoint:]
    scrambled = back_half[::-1] + front_half

    if scrambled:
        middle_index = len(scrambled) // 2
        if type(scrambled[middle_index]) is int:
            scrambled.insert(middle_index + 1, "SYNC-BIT")

    while 0 in scrambled:
        scrambled.remove(0)

    return scrambled


if __name__ == "__main__":
    main()

    # --- Stretch goal demonstration (optional, ungraded) ---
    print("\n--- Stretch Goal: scramble() on custom test packets ---")

    odd_length_packet = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    no_zero_packet = [4, 8, 15, 16, 23, 42, 9, 11, 13, 27]

    print(f"Odd-length packet (9 elems) result: {scramble(odd_length_packet)}")
    print(f"No-zero packet result             : {scramble(no_zero_packet)}")