# 🏗️ Named Parameters Architecture — Visual Documentation

**Date:** January 17, 2026  
**Purpose:** Visual explanations of the CGAL Named Parameters system flow  
**Author:** Utkarsh Khajuria

---

## 📋 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Data Flow Diagram](#-data-flow-diagram)
- [Multi-Parameter Processing](#-multi-parameter-processing)
- [Operator Pattern Flowchart](#-operator-pattern-flowchart)
- [Wrapper std::apply Visualization](#-wrapper-stdapply-visualization)
- [Type Casting Flow](#-type-casting-flow)
- [Parameter Chaining](#-parameter-chaining)
- [Complete Annotated Example](#-complete-annotated-example)

---

## 🔄 Architecture Overview

The Named Parameters system bridges Python dictionaries to CGAL's compile-time parameter chains through a sophisticated multi-layer architecture.

### System Flow Diagram

```mermaid
flowchart TB
    subgraph Python["🐍 PYTHON LAYER"]
        A["PMP.compute_face_normals(mesh, fnormals, {'geom_traits': kernel})"]
        B["py::dict params = {'geom_traits': kernel}"]
    end
    
    subgraph Binding["⚙️ BINDING LAYER (C++)"]
        C["auto np = CGAL::parameters::default_values()"]
        D["CGALPY::Named_parameter_geom_traits op"]
        E["Named_parameter_wrapper&lt;...&gt; wrapper(mesh, fnormals)"]
        F["named_parameter_applicator(wrapper, np, params, op)"]
    end
    
    subgraph Applicator["🔁 APPLICATOR (Recursive)"]
        G{"for item in params:
        item.key == op.m_name?"}
        H["np_new = op(np, item.value)"]
        I["Recurse with np_new"]
        J["Base case: wrapper(np_final)"]
    end
    
    subgraph Operator["📦 OPERATOR"]
        K["struct Named_parameter_geom_traits"]
        L["return np.geom_traits(py::cast&lt;const Kernel&&gt;(value))"]
    end
    
    subgraph Wrapper["📋 WRAPPER"]
        M["std::apply with stored tuple (mesh, fnormals)"]
        N["Compute_face_normals_wrapper::call(np, mesh, fnormals)"]
    end
    
    subgraph CGAL["🎯 CGAL LAYER"]
        O["PMP::compute_face_normals(mesh, fnormals, CGAL::parameters::geom_traits(kernel))"]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G -->|"✅ Match!"| H
    H --> K
    K --> L
    L --> I
    I --> J
    J --> M
    M --> N
    N --> O
```

---

## 📊 Data Flow Diagram

### How Python Dict Becomes CGAL Parameters

```mermaid
flowchart LR
    subgraph Input["📥 Python Dict"]
        D1["'geom_traits': kernel"]
        D2["'verbose': true"]
        D3["'vertex_map': vm"]
    end
    
    subgraph Matching["🎯 Operator Matching"]
        M1["op.m_name == 'geom_traits' ✓"]
        M2["op.m_name == 'verbose' ✓"]
        M3["op.m_name == 'vertex_map' ✓"]
    end
    
    subgraph Chaining["🔗 Parameter Chain"]
        C1["np.geom_traits(k)"]
        C2[".verbose(true)"]
        C3[".vertex_map(vm)"]
    end
    
    subgraph Final["✨ Final Result"]
        F["CGAL::parameters::geom_traits(k).verbose(true).vertex_map(vm)"]
    end
    
    D1 --> M1 --> C1
    D2 --> M2 --> C2
    D3 --> M3 --> C3
    C1 & C2 & C3 --> F
```

---

## 🔢 Multi-Parameter Processing

When a Python call includes multiple parameters, the applicator processes each one recursively:

### Step-by-Step Processing

```mermaid
sequenceDiagram
    participant Python as 🐍 Python
    participant Applicator as 🔁 Applicator
    participant Op1 as 📦 Op1 (vertex_point_map)
    participant Op2 as 📦 Op2 (geom_traits)
    participant Op3 as 📦 Op3 (verbose)
    participant Wrapper as 📋 Wrapper
    participant CGAL as 🎯 CGAL
    
    Python->>Applicator: params = {vpm, kernel, True}
    
    Note over Applicator: Process item 1: "vertex_point_map"
    Applicator->>Op1: Does "vertex_point_map" match?
    Op1-->>Applicator: ✅ Match! Return np.vertex_point_map(vpm)
    
    Note over Applicator: Recurse with np_new
    Applicator->>Op2: Does "geom_traits" match?
    Op2-->>Applicator: ✅ Match! Return np_new.geom_traits(kernel)
    
    Note over Applicator: Recurse with np_newer
    Applicator->>Op3: Does "verbose" match?
    Op3-->>Applicator: ✅ Match! Return np_newer.verbose(true)
    
    Note over Applicator: No more operators - Base case
    Applicator->>Wrapper: wrapper(np_final)
    Wrapper->>CGAL: PMP::function(mesh, fn, np_final)
```

### Parameter Chain Building

```mermaid
graph TD
    subgraph Step1["Step 1: Empty Chain"]
        A["np = CGAL::parameters::default_values()"]
        A1["📦 Empty chain"]
    end
    
    subgraph Step2["Step 2: After vertex_point_map"]
        B["np_new = np.vertex_point_map(vpm)"]
        B1["📦 vertex_point_map: vpm"]
    end
    
    subgraph Step3["Step 3: After geom_traits"]
        C["np_newer = np_new.geom_traits(kernel)"]
        C1["📦 vertex_point_map: vpm<br/>📦 geom_traits: kernel"]
    end
    
    subgraph Step4["Step 4: After verbose"]
        D["np_final = np_newer.verbose(true)"]
        D1["📦 vertex_point_map: vpm<br/>📦 geom_traits: kernel<br/>📦 verbose: true"]
    end
    
    A --> A1
    A1 -->|"op1()"| B
    B --> B1
    B1 -->|"op2()"| C
    C --> C1
    C1 -->|"op3()"| D
    D --> D1
    
    style D1 fill:#90EE90
```

> **Note:** This is compile-time chaining! Each `.parameter()` call returns a new type with that parameter baked in.

---

## 🔀 Operator Pattern Flowchart

### Choosing the Right Pattern

```mermaid
flowchart TD
    Start["🎬 START: Need to bind Named Parameter"]
    
    Q1{"What type is<br/>the parameter?"}
    
    P1["📌 Pattern 1<br/>Simple Value<br/>(bool, int, double)"]
    P2["📌 Pattern 2<br/>Property Map"]
    P3["📌 Pattern 3<br/>Kernel/Traits"]
    P4["📌 Pattern 4<br/>Functor"]
    P5["📌 Pattern 5<br/>Complex Object"]
    
    Create["✍️ Create operator struct<br/>• Set m_name<br/>• Implement operator()<br/>• Add type casting<br/>• Return chained np"]
    
    Test["🧪 Test with simple function"]
    Register["📝 Add to operator registry"]
    End["✅ END"]
    
    Start --> Q1
    Q1 -->|"bool/int/double"| P1
    Q1 -->|"Property map"| P2
    Q1 -->|"geom_traits"| P3
    Q1 -->|"std::function"| P4
    Q1 -->|"Custom CGAL type"| P5
    
    P1 & P2 & P3 & P4 & P5 --> Create
    Create --> Test
    Test --> Register
    Register --> End
    
    style P1 fill:#87CEEB
    style P2 fill:#98FB98
    style P3 fill:#DDA0DD
    style P4 fill:#F0E68C
    style P5 fill:#FFA07A
```

---

## 📦 Wrapper std::apply Visualization

The `Named_parameter_wrapper` stores function arguments in a tuple and uses `std::apply` to unpack them:

### Tuple Storage and Unpacking

```mermaid
graph TB
    subgraph Storage["📦 Named_parameter_wrapper Storage"]
        T["std::tuple&lt;Mesh&, FNMap&&gt;"]
        T1["┌────────┐"]
        T2["│  mesh  │"]
        T3["├────────┤"]
        T4["│ fnorm  │"]
        T5["└────────┘"]
    end
    
    subgraph Call["📞 wrapper(np) Called"]
        C["std::apply(lambda, tuple)"]
    end
    
    subgraph Lambda["λ Lambda Execution"]
        L1["[&np](Mesh& m, FNMap& fn)"]
        L2["↓ unpack ↓"]
        L3["m = mesh (from tuple)"]
        L4["fn = fnormals (from tuple)"]
    end
    
    subgraph Final["🎯 Final Call"]
        F["Compute_face_normals_wrapper::call(np, mesh, fnormals)"]
    end
    
    T --> T1 --> T2 --> T3 --> T4 --> T5
    T5 --> C
    C --> L1
    L1 --> L2
    L2 --> L3
    L2 --> L4
    L3 & L4 --> F
```

### Code Flow

```cpp
// wrapper.data contains:
std::tuple<const Mesh&, const FNMap&>(mesh, fnormals)

// When wrapper(np) is called:
return std::apply(
    [&np](const Mesh& mesh, const FNMap& fnormals) {
        //     ↑↑↑↑↑↑↑↑↑↑    ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
        //     Unpacked from tuple automatically!
        
        return Compute_face_normals_wrapper::call(
            np,        // Built parameter chain
            mesh,      // From tuple
            fnormals   // From tuple
        );
    },
    std::move(wrapper.data)  // The tuple to unpack
);
```

---

## 🔄 Type Casting Flow

### Python to C++ Type Conversions

```mermaid
graph LR
    subgraph Python["🐍 Python Value"]
        P1["kernel (object)"]
        P2["vpm (property map)"]
        P3["True (boolean)"]
        P4["100 (integer)"]
        P5["0.01 (float)"]
        P6["func (lambda)"]
    end
    
    subgraph Cast["⚡ nanobind Cast"]
        C1["py::cast&lt;const Kernel&&gt;"]
        C2["Generic (nanobind)"]
        C3["py::cast&lt;bool&gt;"]
        C4["py::cast&lt;std::size_t&gt;"]
        C5["py::cast&lt;double&gt;"]
        C6["py::cast&lt;std::function&lt;...&gt;&gt;"]
    end
    
    subgraph CPP["🔧 C++ Type"]
        T1["const Kernel&"]
        T2["Property_map&lt;Vd, Point&gt;"]
        T3["bool"]
        T4["std::size_t"]
        T5["double"]
        T6["std::function&lt;bool(Vd,P,P)&gt;"]
    end
    
    P1 --> C1 --> T1
    P2 --> C2 --> T2
    P3 --> C3 --> T3
    P4 --> C4 --> T4
    P5 --> C5 --> T5
    P6 --> C6 --> T6
```

---

## 🔗 Parameter Chaining

### Visual Representation

```mermaid
graph TD
    subgraph Chain["Parameter Chain Building"]
        Start["🏁 Start: Empty"]
        
        S1["np = default_values()"]
        S1V["📦 (empty)"]
        
        S2["np.vertex_point_map(vpm)"]
        S2V["📦 vertex_point_map: vpm"]
        
        S3[".geom_traits(kernel)"]
        S3V["📦 vertex_point_map: vpm<br/>📦 geom_traits: kernel"]
        
        S4[".verbose(true)"]
        S4V["📦 vertex_point_map: vpm<br/>📦 geom_traits: kernel<br/>📦 verbose: true"]
    end
    
    Start --> S1
    S1 --> S1V
    S1V --> S2
    S2 --> S2V
    S2V --> S3
    S3 --> S3V
    S3V --> S4
    S4 --> S4V
    
    style S4V fill:#90EE90,stroke:#228B22,stroke-width:2px
```

---

## 📚 Variadic Template Recursion

The `named_parameter_applicator` uses variadic templates to process operators recursively:

```mermaid
flowchart TB
    subgraph Call["Initial Call"]
        A["named_parameter_applicator(wrapper, np, params, op1, op2, op3)"]
    end
    
    subgraph Iter1["Iteration 1"]
        B["Process params with op1"]
        B1{"Match?"}
        B2["call op1, recurse with (op2, op3)"]
        B3["recurse with (op2, op3)"]
    end
    
    subgraph Iter2["Iteration 2"]
        C["Process params with op2"]
        C1{"Match?"}
        C2["call op2, recurse with (op3)"]
        C3["recurse with (op3)"]
    end
    
    subgraph Iter3["Iteration 3"]
        D["Process params with op3"]
        D1{"Match?"}
        D2["call op3, recurse with ()"]
        D3["recurse with ()"]
    end
    
    subgraph Base["Base Case"]
        E["No more operators"]
        F["wrapper(np_final)"]
        G["Execute CGAL function ✅"]
    end
    
    A --> B
    B --> B1
    B1 -->|"Yes"| B2
    B1 -->|"No"| B3
    B2 --> C
    B3 --> C
    C --> C1
    C1 -->|"Yes"| C2
    C1 -->|"No"| C3
    C2 --> D
    C3 --> D
    D --> D1
    D1 -->|"Yes"| D2
    D1 -->|"No"| D3
    D2 --> E
    D3 --> E
    E --> F
    F --> G
    
    style G fill:#90EE90
```

---

## 📝 Complete Annotated Example

### Full Flow with Code Comments

```cpp
// ═══════════════════════════════════════════════════════════════════
// 🐍 PYTHON CALL
// ═══════════════════════════════════════════════════════════════════
PMP.compute_face_normals(mesh, fnormals, {"geom_traits": kernel})

// ═══════════════════════════════════════════════════════════════════
// ⚙️ C++ BINDING FUNCTION
// ═══════════════════════════════════════════════════════════════════
template <typename Mesh, typename FNMap>
void compute_face_normals(Mesh& m, FNMap& fn, py::dict params) {
  
  // 📌 Step 1: Start with empty parameter chain
  auto np = CGAL::parameters::default_values();
  //   np type: Named_function_parameters<...>
  
  // 📌 Step 2: Create operator for geom_traits parameter
  CGALPY::Named_parameter_geom_traits op;
  //   op.m_name = "geom_traits"
  //   op.operator() will cast value and chain .geom_traits()
  
  // 📌 Step 3: Create wrapper storing function arguments
  CGALPY::Named_parameter_wrapper<
    Compute_face_normals_wrapper,  // Function wrapper template
    const Mesh&,                    // Arg 1 type
    const FNMap&                    // Arg 2 type
  > wrapper(m, fn);
  //   wrapper.data = std::tuple<const Mesh&, const FNMap&>(m, fn)
  
  // 📌 Step 4: Process parameters and execute
  CGALPY::named_parameter_applicator(
    wrapper,    // Stores mesh + fnormals
    np,         // Empty parameter chain
    params,     // {"geom_traits": kernel}
    op          // Operator to try
  );
}

// ═══════════════════════════════════════════════════════════════════
// 🔁 INSIDE APPLICATOR
// ═══════════════════════════════════════════════════════════════════
for (auto& item : params) {
    std::string key = py::cast<std::string>(item.first);
    // key = "geom_traits"
    
    if (key == op.m_name) {  // "geom_traits" == "geom_traits" ✓
        // MATCH! Call operator
        auto np_new = op(np, item.second);
        //   op(np, kernel)
        //   → np.geom_traits(py::cast<const Kernel&>(kernel))
        //   → Returns updated parameter chain
        
        // Recurse with updated chain (no more operators = base case)
        return named_parameter_applicator(wrapper, np_new, params);
    }
}

// ═══════════════════════════════════════════════════════════════════
// 📦 BASE CASE - CALL WRAPPER
// ═══════════════════════════════════════════════════════════════════
return wrapper(np_new);

// ═══════════════════════════════════════════════════════════════════
// 📋 INSIDE WRAPPER.OPERATOR()
// ═══════════════════════════════════════════════════════════════════
return std::apply(
    [&np_new](const Mesh& mesh, const FNMap& fnormals) {
        // Unpack tuple args: mesh, fnormals
        return Compute_face_normals_wrapper::call(
            np_new,    // Parameter chain: .geom_traits(kernel)
            mesh,      // From tuple
            fnormals   // From tuple
        );
    },
    std::move(wrapper.data)  // Move tuple
);

// ═══════════════════════════════════════════════════════════════════
// 🎯 FINAL CGAL CALL
// ═══════════════════════════════════════════════════════════════════
static void call(auto np, const Mesh& m, const FNMap& fn) {
    // Reorder: Named Parameters go LAST for CGAL
    PMP::compute_face_normals(
        m,   // Arg 1
        fn,  // Arg 2  
        np   // Named Parameters (last!)
    );
}

// ✅ CGAL function executes with proper parameters!
PMP::compute_face_normals(
    mesh,
    fnormals,
    CGAL::parameters::geom_traits(kernel)  // Compile-time parameter
);
```

---

## 🎯 Summary

The Named Parameters architecture consists of:

| Component | Purpose | Key Feature |
|-----------|---------|-------------|
| **Python Layer** | Accept dict from user | `{"param": value}` |
| **Binding Layer** | Initialize wrapper + operators | Template setup |
| **Applicator** | Match dict keys to operators | Recursive processing |
| **Operators** | Type-cast and chain parameters | `np.param(value)` |
| **Wrapper** | Store args, call function | `std::apply` magic |
| **CGAL Layer** | Execute algorithm | Compile-time params |

---

**Last Updated:** January 17, 2026  
**Status:** ✅ Architecture fully documented with visual diagrams