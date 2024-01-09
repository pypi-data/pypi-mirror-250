// Copyright 2018-2023 Xanadu Quantum Technologies Inc.

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "ObservablesGPUMPI.hpp"
#include "StateVectorCudaMPI.hpp"

using namespace Pennylane::LightningGPU;

template class Observables::NamedObsMPI<StateVectorCudaMPI<float>>;
template class Observables::NamedObsMPI<StateVectorCudaMPI<double>>;

template class Observables::HermitianObsMPI<StateVectorCudaMPI<float>>;
template class Observables::HermitianObsMPI<StateVectorCudaMPI<double>>;

template class Observables::TensorProdObsMPI<StateVectorCudaMPI<float>>;
template class Observables::TensorProdObsMPI<StateVectorCudaMPI<double>>;

template class Observables::HamiltonianMPI<StateVectorCudaMPI<float>>;
template class Observables::HamiltonianMPI<StateVectorCudaMPI<double>>;

template class Observables::SparseHamiltonianMPI<StateVectorCudaMPI<float>>;
template class Observables::SparseHamiltonianMPI<StateVectorCudaMPI<double>>;
