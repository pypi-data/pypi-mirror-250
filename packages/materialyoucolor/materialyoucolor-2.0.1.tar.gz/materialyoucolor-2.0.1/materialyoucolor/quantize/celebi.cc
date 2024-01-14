/*
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "celebi.h"

#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <vector>

#include "wsmeans.h"
#include "wu.h"
#include "utils.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace python = pybind11;

// std::map<Argb, uint32_t>
std::map<uint32_t, uint32_t> QuantizeCelebi(const python::list& pixels,
                               int max_colors) {
  if (max_colors > 256) {
    max_colors = 256;
  }

  int pixel_count = pixels.size();

  std::vector<material_color_utilities::Argb> opaque_pixels;
  opaque_pixels.reserve(pixel_count);
  for (int i = 0; i < pixel_count; i++) {
    python::list rgba_ = python::cast<python::list>(pixels[i]);
    uint32_t pixel = (python::cast<uint32_t>(rgba_[0])  << 16) | 
                     (python::cast<uint32_t>(rgba_[1])  << 8) | 
                     python::cast<uint32_t>(rgba_[2]);
    opaque_pixels.push_back(pixel);
  }

  std::vector<material_color_utilities::Argb> wu_result = material_color_utilities::QuantizeWu(opaque_pixels, max_colors);

  material_color_utilities::QuantizerResult result =
      material_color_utilities::QuantizeWsmeans(opaque_pixels, wu_result, max_colors);
  
  return result.color_to_count;
}



PYBIND11_MODULE(celebi, m) {
    m.doc() = "QuantizeCelebi from cpp";
    m.def("QuantizeCelebi", &QuantizeCelebi, "Get dominant colors");
}
