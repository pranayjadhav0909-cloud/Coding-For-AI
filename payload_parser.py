"""
Coding for AI - Problem Set 7: Payload Packet Parser

HEADER NOTE- 
'/' and '*' in the signature: parameters before '/' (raw_packet, delimiter)
are positional-only, so they can never be passed as keywords -- this hides
their names as an implementation detail. Parameters after '*'
(correction_offset) are keyword-only, so they must always be named at the
call site -- this prevents same-typed arguments from being swapped by
accident.
 
Why slicing avoids aliasing: raw_packet[1][:] always builds a brand-new list
object, distinct from raw_packet[1]. Iterating over that new list inside a
comprehension then produces yet another new list. So the returned list never
shares identity with the original, giving an import-free deep copy.
"""

def parse_payload(raw_packet: list, delimiter: str, /, *,
                   correction_offset: int = 0) -> tuple:
    status_tokens = raw_packet[2].split(delimiter)
    corrected_sensors = [
        value if "ERROR" in status_tokens else value + correction_offset
        for value in raw_packet[1][:]
    ]
    return raw_packet[0], corrected_sensors


if __name__ == "__main__":
    packet_1 = [501, [12.5, 13.0, 11.8], "NOMINAL|CALIBRATED"]
    packet_2 = [502, [9.0, 8.5], "ERROR|SENSOR_FAULT"]
    packet_3 = [503, [1.0, 2.0], "NOMINAL"]
    packet_4 = [504, [], "NOMINAL"]
    packet_5 = [505, [10.0, 20.0, 30.0], "NOMINAL|CALIBRATED|LOW_POWER"]

    result_1 = parse_payload(packet_1, "|", correction_offset=2)
    print("Test 1 ->", result_1[0], result_1[1])
    assert packet_1[1] == [12.5, 13.0, 11.8], "Original packet_1 sensors were mutated!"
    assert result_1[1] is not packet_1[1], "Returned list must be a different object!"
    assert id(result_1[1]) != id(packet_1[1]), "Returned list must have a different id!"
    print("Test 1 side-effect assertions passed.")

    result_2 = parse_payload(packet_2, "|", correction_offset=5)
    print("Test 2 ->", result_2[0], result_2[1])
    assert packet_2[1] == [9.0, 8.5], "Original packet_2 sensors were mutated!"
    assert result_2[1] is not packet_2[1], "Returned list must be a different object!"
    assert result_2[1] == packet_2[1], "Values should be unchanged when ERROR is present!"
    print("Test 2 side-effect assertions passed.")

    result_3 = parse_payload(packet_3, "|")
    print("Test 3 (default offset) ->", result_3[0], result_3[1])
    assert result_3[1] == [1.0, 2.0], "Default offset of 0 should leave values unchanged!"

    result_3b = parse_payload(packet_3, "|", correction_offset=0)
    print("Edge case (offset=0 explicit) ->", result_3b[0], result_3b[1])
    assert result_3b[1] == result_3[1], "Explicit offset=0 must behave like the default!"
    print("Edge case passed: offset=0 explicit matches offset omitted.")

    result_4 = parse_payload(packet_4, "|", correction_offset=3)
    print("Edge case (empty sensor list) ->", result_4[0], result_4[1])
    assert result_4[1] == [], "Empty sensor list should return an empty list!"
    print("Edge case passed: empty sensor list handled without error.")

    result_5 = parse_payload(packet_5, "|", correction_offset=1)
    print("Edge case (3+ status codes) ->", result_5[0], result_5[1])
    assert result_5[1] == [11.0, 21.0, 31.0], "Multi-token status parsing failed!"
    print("Edge case passed: multi-token status flag parsed correctly.")

    try:
        parse_payload(raw_packet=packet_1, delimiter="|")
        raise AssertionError("Test 4 failed: no TypeError was raised!")
    except TypeError as e:
        print("Test 4 passed. TypeError raised as expected:", e)

    try:
        parse_payload(packet_1, "|", 2)
        raise AssertionError("Test 5 failed: no TypeError was raised!")
    except TypeError as e:
        print("Test 5 passed. TypeError raised as expected:", e)
