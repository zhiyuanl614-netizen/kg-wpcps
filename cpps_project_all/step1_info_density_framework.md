# Step 1: Five Material Types Information Density Framework
> v1.0 | 2026-08-31

## Key Findings Summary

### 1. Academic Paper Simplification Pattern (CRITICAL)
Industry Knowledge -> Paper Actual Usage:
- Substation -> Bus (node)
- TransmissionLine/DistributionLine -> Branch
- Transformer -> Branch impedance
- Breaker -> Branch on/off state
- PumpStation -> Pump + mapped to Bus
- WaterTreatmentPlant -> Node (source)
- Pipeline -> Pipe/Link
- Valve -> Pipe state (open/closed)
- Tank/Reservoir -> Tank (node)
- SCADA/PLC/RTU/PMU -> CyberNode
- Sensor/Actuator -> CyberNode attribute
- CommLink -> CyberEdge

### 2. Core Coupling Relationship
POWERED_BY (Pump -> Bus) appears in 4/5 material types, explicitly given in nearly 100% of papers.

### 3. Cyber Layer Simplification
All material types simplify cyber layer:
- Papers: CyberNode (single type)
- Reports/Plans/Events: mention SCADA only
- Standards: require monitoring/control only
-> Ontology: CyberNode + CommLink only, no PLC/RTU/PMU subdivision

### 4. v1.0 Attributes to DELETE (0 material types can extract)
- latitude/longitude
- ip_address
- firmware_version

### 5. Station <-> Node Bidirectional Mapping Required
Papers use Bus/Pump, Plans use Substation/PumpStation
Mapping: PumpStation CONTAINS Pump; Substation CONTAINS Bus

### 6. Cascade Chain Two Expression Modes
Narrative (M4/M5): substation outage -> pump trip -> pressure drop
Model (M1): Bus-5 fault -> Pump-3 loss -> Node-12 pressure < 0.15MPa

## Seven-Dimension Analysis Framework

D1-Entity Granularity: L1(system) L2(station) L3(device) L4(node) L5(component)
D2-Attribute Precision: A0(none) A1(qualitative) A2(semi-quantitative) A3(rated) A4(simulation) A5(realtime)
D3-Relationship Explicitness: R0(implicit) R1(qualitative) R2(named) R3(formula) R4(probabilistic)
D4-Spatio-Temporal: T1(year/province) T2(date/city) T3(hour/station) T4(minute/device) T5(sim-step/node)
D5-CPS Coupling: C0(none) C1(mention) C2(simplified) C3(layered) C4(protocol)
D6-Cascade Mechanism: F0(none) F1(narrative) F2(topological) F3(physical-model) F4(probabilistic)
D7-Quantification: Q0(qualitative) Q1(statistics) Q2(index) Q3(simulation) Q4(parametric-model)

## Material Type Comparison Matrix

| Dimension | M1-Paper | M2-Report | M3-Standard | M4-Plan | M5-Event |
|-----------|----------|-----------|-------------|---------|----------|
| D1 | L4-node | L2-station | L2-station | L2-station | L2-station |
| D2 | A4-simulation | A2-semi | A3-rated | A2-semi | A1-qualitative |
| D3 | R3-formula | R1-qualitative | R1-qualitative | R2-named | R0-implicit |
| D4 | T5-sim-step | T1-year | T1-year | T2-date | T2-date |
| D5 | C2-simplified | C1-mention | C0-none | C1-mention | C1-mention |
| D6 | F3-physical | F1-narrative | F0-none | F1-narrative | F1-narrative |
| D7 | Q4-parametric | Q1-statistics | Q2-index | Q1-statistics | Q1-statistics |

## Entity Cross-Material Matrix

| Entity | M1 | M2 | M3 | M4 | M5 | Count |
|--------|----|----|----|----|----|-------|
| Bus | Y | N | N | N | N | 1 |
| Branch | Y | N | N | N | N | 1 |
| Generator | Y | N | N | N | N | 1 |
| Pump | Y | Y | Y | Y | Y | 5 |
| Pipe/Link | Y | N | Y | N | N | 2 |
| Tank | Y | Y | Y | Y | Y | 5 |
| Node/Junction | Y | N | N | N | N | 1 |
| Substation | ->Bus | Y | Y | Y | Y | 4 |
| PowerPlant | ->Gen | Y | Y | N | Y | 3 |
| WaterTreatmentPlant | ->Node | Y | Y | Y | Y | 4 |
| PumpStation | ->Pump+Bus | Y | Y | Y | Y | 4 |
| CyberNode | Y | N | N | N | N | 1 |
| SCADA(mention) | Y | Y | Y | Y | Y | 5 |
| HazardType | Y | Y | Y | Y | Y | 5 |
| CascadeChain | Y | Y | N | Y | Y | 4 |

## Relationship Cross-Material Matrix

| Relationship | M1 | M2 | M3 | M4 | M5 | Count |
|-------------|----|----|----|----|----|-------|
| POWERED_BY(Pump->Bus) | Y-formula | Y-qualitative | N | Y-named | Y-narrative | 4 |
| CONNECTS_TO | Y-topology | N | Y-spec | N | N | 2 |
| CASCADES_TO | Y-model | Y-narrative | N | Y-narrative | Y-narrative | 4 |
| CONTROLS | Y-simplified | Y-mention | Y-require | Y-mention | N | 3 |
| MONITORS | Y-simplified | Y-mention | Y-require | Y-mention | N | 3 |
| TRIGGERS | Y-probability | Y-qualitative | N | Y-qualitative | Y-narrative | 4 |
| DEPENDS_ON | Y-formula | Y-qualitative | Y-require | Y-named | Y-narrative | 5 |
| HAS_BACKUP | N/binary | Y | Y-require | Y-detailed | Y | 4 |

## Attribute Cross-Material Matrix

| Attribute | M1 | M2 | M3 | M4 | M5 | Count | v2.0 |
|-----------|----|----|----|----|----|-------|------|
| voltage_level | A4 | A2 | A3 | A2 | A1 | 5 | KEEP |
| rated_capacity | A4 | A2 | A3 | N | N | 3 | KEEP |
| pump_power/head | A4 | A2 | A3 | N | N | 3 | KEEP |
| pipe_diameter/length | A4 | N | A3 | N | N | 2 | KEEP(optional) |
| backup_power_type | N/binary | A1 | A2 | A2 | A1 | 4 | KEEP |
| backup_duration | N | N | A2 | A2 | A1 | 3 | KEEP |
| coordinates | N | N | N | N | N | 0 | DELETE |
| ip_address | N | N | N | N | N | 0 | DELETE |
| firmware_version | N | N | N | N | N | 0 | DELETE |
| comm_protocol | N | N | A2 | N | N | 1 | DOWNGRADE |
| sim_model_type | Y | N | N | N | N | 1 | KEEP(paper-only) |
| cascade_probability | A4 | N | N | N | N | 1 | KEEP(paper-only) |
| resilience_index | A4 | A2 | N | N | N | 2 | KEEP |
| affected_population | N | A2 | N | N | A2 | 2 | KEEP |
| recovery_time | N | A2 | N | A2 | A2 | 3 | KEEP |

## Ontology Construction Constraints

| ID | Constraint | Source |
|----|-----------|--------|
| C1 | Physical layer: station-level + node-level granularity with bidirectional mapping | D1 |
| C2 | Paper simplification: Substation->Bus, PumpStation->Pump+Bus | M1 |
| C3 | Cyber layer: CyberNode + CommLink only, no PLC/RTU/PMU subdivision | D5 |
| C4 | POWERED_BY(Pump->Bus) as core anchor relationship | Cross-matrix |
| C5 | All attributes must be extractable from >=1 material type | D2 |
| C6 | Delete coordinates/IP/firmware fields | Cross-matrix |
| C7 | Define material-type-specific extraction strategies | D1-D7 |
| C8 | Cascade chain supports narrative and model expression | D6 |
