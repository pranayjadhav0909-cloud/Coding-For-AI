#LOGIC TRACE (Deliverable-2)

##A Python "for" loop is completely different from a C-style loop.
##A C-style loop uses a manual counter and a condition that you write
##yourself, so if you mess up the condition the loop can spin forever.
##A Python "for" loop just walks through the items of whatever sequence
##you give it, one by one, and stops automatically the moment it runs
##out of items. If a batch is an empty list [], then it has zero items
##to walk through, so the inner "for reading in batch:" loop body
##simply never executes even a single time - the loop finishes
##immediately on its own. There is no counter to forget to update and
##no condition to get wrong, so there is no way for the program to
##hang. The outer loop then just moves on to the next batch_id as
##normal, and (assuming no STOP was seen) the else block still runs
##because the outer loop was never broken out of.


telemetry_stream = [
    [22.5, 23.0, 22.8],
    [25.1, "ERR", 24.9],
    [30.2, 35.5, 40.1],   # Threshold breach
    [22.0, 22.1, "STOP"],  # Termination signal
]

THRESHOLD = 35.0
SPIKE_DELTA = 5.0

shutdown_triggered = False

for batch_id in range(len(telemetry_stream)):
    batch = telemetry_stream[batch_id]
    print(f"--- Auditing Batch {batch_id}: {batch} ---")

    previous_value = None

    for reading in batch:

        # Order of checks matters: STOP first, then ERR, then numeric.
        if reading == "STOP":
            print(f"Emergency Shutdown at Batch {batch_id}.")
            shutdown_triggered = True
            break  # exits only the INNER loop

        if reading == "ERR":
            print(f"Noise ignored at Batch {batch_id} (ERR).")
            continue  # skip this reading, move to the next one

        if isinstance(reading, (int, float)):

            # Threshold check (core requirement).
            if reading > THRESHOLD:
                print(f"Anomaly Detected at Batch {batch_id}: {reading}")

            if previous_value is not None:
                delta = abs(reading - previous_value)
                if delta > SPIKE_DELTA:
                    print(
                        f"Spike Detected at Batch {batch_id}: "
                        f"{previous_value} -> {reading} (Delta {round(delta, 1)})"
                    )

            # Update previous_value only after a successful numeric
            # comparison, as the assignment hint instructs.
            previous_value = reading


    if shutdown_triggered:
        break

else:
    # This else belongs to the OUTER for loop. Python only skips it
    # if the outer loop was exited with break, which only happens
    # when shutdown_triggered is True.
    print("Audit Complete: No system-wide failures")


    
