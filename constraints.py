from ortools.sat.python import cp_model

# Instantiate model and solver
model = cp_model.CpModel()
solver = cp_model.CpSolver()

freqs = {
    0: "f0",
    1: "f1",
    2: "f2"
}

# Setup nodes/antennae
Antenna1 = model.NewIntVar(0,2, "A1")
Antenna2 = model.NewIntVar(0,2, "A2")
Antenna3 = model.NewIntVar(0,2, "A3")
Antenna4 = model.NewIntVar(0,2, "A4")
Antenna5 = model.NewIntVar(0,2, "A5")
Antenna6 = model.NewIntVar(0,2, "A6")
Antenna7 = model.NewIntVar(0,2, "A7")
Antenna8 = model.NewIntVar(0,2, "A8")
Antenna9 = model.NewIntVar(0,2, "A9")

# Add edges/constraints
model.Add(Antenna1 != Antenna2)
model.Add(Antenna1 != Antenna3)
model.Add(Antenna1 != Antenna4)
model.Add(Antenna2 != Antenna3)
model.Add(Antenna2 != Antenna5)
model.Add(Antenna2 != Antenna6)
model.Add(Antenna3 != Antenna6)
model.Add(Antenna3 != Antenna9)
model.Add(Antenna4 != Antenna2)
model.Add(Antenna4 != Antenna5)
model.Add(Antenna6 != Antenna7)
model.Add(Antenna6 != Antenna8)
model.Add(Antenna7 != Antenna8)
model.Add(Antenna8 != Antenna9)

status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print("Antenna1: %s" % freqs[solver.Value(Antenna1)])
    print("Antenna2: %s" % freqs[solver.Value(Antenna2)])
    print("Antenna3: %s" % freqs[solver.Value(Antenna3)])
    print("Antenna4: %s" % freqs[solver.Value(Antenna4)])
    print("Antenna5: %s" % freqs[solver.Value(Antenna5)])
    print("Antenna6: %s" % freqs[solver.Value(Antenna6)])
    print("Antenna7: %s" % freqs[solver.Value(Antenna7)])
    print("Antenna8: %s" % freqs[solver.Value(Antenna8)])
    print("Antenna9: %s" % freqs[solver.Value(Antenna9)])
