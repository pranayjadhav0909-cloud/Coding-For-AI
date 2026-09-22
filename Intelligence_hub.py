"""
HEADER DOCUMENTATION-
Why setdefault for the Movement Log:
    On an agent's first move, its key isn't in `movement_log` yet, so a plain
    `.append()` would raise a KeyError. `setdefault(agent_id, [])` inserts an
    empty list only if the key is missing, then returns that list either way -
    so one line handles both the first move and every move after it, no
    "if not in" check needed.
 
Why a tuple (not a list) for Location:
    A tuple is immutable, so a coordinate pair can't be changed in place by
    other code reaching into it (e.g. `location[0] = 99`). That guarantees
    the agent's position stays consistent until it's deliberately replaced.
    A list would allow silent, untracked edits. The only way to "move" an
    agent is to build a new tuple and reassign it - exactly what
    `relocate_agent` does.
 
SUBMISSION NOTE-
`registry[agent_id]["Location"][0] = ...` raises
`TypeError: 'tuple' object does not support item assignment`. Lists are
mutable containers - their memory slots can be overwritten directly, so
`list[0] = x` is legal. Tuples are fixed sequences: once built, Python
doesn't provide any operation to overwrite an element in place. The error
isn't a bug; it's the language enforcing that a tuple's contents never
change during its lifetime. The only way to "change" one is to construct a
new tuple and rebind the name (or key) to it - which is what
`relocate_agent` does when it reassigns the whole "Location" entry.
"""


# Nested State Registry
agent_registry = {
    "Agent_Alpha": {
        "Location": (10, 20),
        "Knowledge": {"grid_map", "comm_protocol", "telemetry_sync"},
    },
    "Agent_Beta": {
        "Location": (15, 5),
        "Knowledge": {"grid_map", "comm_protocol", "power_grid"},
    },
    "Agent_Gamma": {
        "Location": (0, 0),
        "Knowledge": {"grid_map", "comm_protocol", "power_grid", "telemetry_sync"},
    },
}

# 3.2 Knowledge Sync Logic
def find_common_intelligence(registry):
    """Return the set of Information Bits known to every agent in `registry`."""
    knowledge_sets = [
        agent_data["Knowledge"] for agent_data in registry.values()
    ]
    # set.intersection(*knowledge_sets) works for any number of sets,
    # including zero or one.
    return set.intersection(*knowledge_sets)


# 3.3 Conflict Resolution and the Immutability Test
def relocate_agent(registry, log, agent_id, new_location):
    
    print(f"Attempting direct mutation of {agent_id}'s Location tuple...")
    try:
        registry[agent_id]["Location"][0] = new_location[0]
    except TypeError as e:
        print(f"TypeError caught: {e}")
        print("Tuples are immutable; reassigning a new tuple instead.")

    # Correct relocation
    registry[agent_id]["Location"] = new_location

    # Movement logging with setdefault
    log.setdefault(agent_id, []).append(new_location)

    print(f"\n{agent_id} new state: {registry[agent_id]}")
    print(f"Movement Log: {log}")


# 3.4 Efficiency Constraint: Summary Report
def build_summary_report(registry):
    """Return a dict mapping AgentID -> number of knowledge bits, via a
    dictionary comprehension (no manual for-loop key assignment)."""
    return {
        agent_id: len(data["Knowledge"])
        for agent_id, data in registry.items()
    }

# Main driver / trace (Section 4)
def main():
    movement_log = {}

    print("--- Full Agent Registry ---")
    print(agent_registry)

    print("\n--- Common Intelligence Across All Agents ---")
    print(find_common_intelligence(agent_registry))

    print("\n--- Relocating Agent_Alpha ---")
    relocate_agent(agent_registry, movement_log, "Agent_Alpha", (12, 22))

    print("\n--- Relocating Agent_Alpha again ---")
    relocate_agent(agent_registry, movement_log, "Agent_Alpha", (14, 25))

    print("\n--- Summary Report (Dictionary Comprehension) ---")
    print(build_summary_report(agent_registry))

    # Edge Cases
    print("\n=== EDGE CASE TESTS ===")

    # Edge Case 1: an agent with an empty Knowledge set.
    print("\n[Edge Case 1] Agent with empty Knowledge set:")
    test_registry_1 = {
        "Agent_Alpha": {"Location": (0, 0), "Knowledge": {"grid_map", "comm_protocol"}},
        "Agent_Empty": {"Location": (1, 1), "Knowledge": set()},
    }
    result_1 = find_common_intelligence(test_registry_1)
    print(f"find_common_intelligence -> {result_1} "
          f"(expected: empty set, since one agent knows nothing)")

    # Edge Case 2: relocating an agent that has never moved before.
    print("\n[Edge Case 2] First-ever move for a fresh agent:")
    fresh_log = {}
    fresh_registry = {
        "Agent_New": {"Location": (5, 5), "Knowledge": {"grid_map"}}
    }
    relocate_agent(fresh_registry, fresh_log, "Agent_New", (6, 6))
    print(f"(expected: Movement Log created on first call, no prior init needed)")

    # Edge Case 3: summary report for an agent with no knowledge yet.
    print("\n[Edge Case 3] Summary report with a zero-knowledge agent:")
    test_registry_3 = {
        "Agent_Blank": {"Location": (0, 0), "Knowledge": set()},
        "Agent_Alpha": {"Location": (0, 0), "Knowledge": {"grid_map", "comm_protocol"}},
    }
    summary_3 = build_summary_report(test_registry_3)
    print(f"build_summary_report -> {summary_3} "
          f"(expected: Agent_Blank -> 0, no error raised)")


if __name__ == "__main__":
    main()
    
