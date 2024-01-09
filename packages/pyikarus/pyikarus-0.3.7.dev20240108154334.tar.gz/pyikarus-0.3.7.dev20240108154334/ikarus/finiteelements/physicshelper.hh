// SPDX-FileCopyrightText: 2021-2024 The Ikarus Developers mueller@ibb.uni-stuttgart.de
// SPDX-License-Identifier: LGPL-3.0-or-later

/**
 * \file physicshelper.hh
 * \brief Material property functions and conversion utilities.
 * \details This file contains material property functions and conversion utilities related to linear elasticity.
 */

#pragma once
#include <dune/common/float_cmp.hh>

#include <Eigen/Core>
namespace Ikarus {

  /**
   * \brief Computes the plane stress linear elastic material tangent matrix.
   *
   * \param E Young's modulus.
   * \param nu Poisson's ratio.
   * \return 3x3 material tangent matrix.
   * \deprecated Use the material library Ikarus::LinearElasticity.
   */
  [[deprecated(
      "These are hard-coded function you should use the material library Ikarus::LinearElasticity")]] inline Eigen::
      Matrix3d
      planeStressLinearElasticMaterialTangent(double E, double nu) {
    Eigen::Matrix3d C;
    C.setZero();
    C(0, 0) = C(1, 1) = 1;
    C(0, 1) = C(1, 0) = nu;
    C(2, 2)           = (1 - nu) / 2;
    C *= E / (1 - nu * nu);
    return C;
  }

  /**
   * \brief Computes the 3D linear elastic material tangent matrix.
   *
   * \param E Young's modulus.
   * \param nu Poisson's ratio.
   * \return 6x6 material tangent matrix.
   * \deprecated Use the material library Ikarus::LinearElasticity.
   */
  [[deprecated(
      "These are hard-coded function you should use the material library: Ikarus::LinearElasticity")]] inline Eigen::
      Matrix<double, 6, 6>
      linearElasticMaterialTangent3D(double E, double nu) {
    Eigen::Matrix<double, 6, 6> C;
    C.setZero();
    C(0, 0) = C(1, 1) = C(2, 2) = 1 - nu;
    C(0, 1) = C(1, 0) = C(2, 0) = C(0, 2) = C(1, 2) = C(2, 1) = nu;
    C(3, 3) = C(4, 4) = C(5, 5) = (1 - 2 * nu) / 2;
    C *= E / ((1 + nu) * (1 - 2 * nu));
    return C;
  }

  /**
   * \brief Traits for handling local views.
   *
   * \tparam LocalView Type of the local view.
   * \tparam useRef Boolean indicating whether to use Eigen::Ref for VectorType and MatrixType.
   */
  template <typename LocalView, bool useRef = false>
  struct TraitsFromLocalView {
    using GridEntity = typename LocalView::Element;
    /** \brief Dimension of the world space */
    static constexpr int worlddim = GridEntity::Geometry::coorddimension;

    /** \brief Dimension of the geometry */
    static constexpr int mydim = GridEntity::mydimension;

    /** \brief Dimension of the grid */
    static constexpr int dimension = GridEntity::dimension;

    /** \brief Type of the internal forces */
    template <typename ScalarType = double>
    using VectorType = std::conditional_t<useRef, Eigen::Ref<Eigen::VectorX<ScalarType>>, Eigen::VectorX<ScalarType>&>;

    /** \brief Type of the stiffness matrix */
    template <typename ScalarType = double>
    using MatrixType = std::conditional_t<useRef, Eigen::Ref<Eigen::MatrixX<ScalarType>>, Eigen::MatrixX<ScalarType>&>;
  };

  ///<  Structure representing Young's modulus and Poisson's ratio. \brief see
  ///<  https://en.wikipedia.org/wiki/Lam%C3%A9_parameters
  struct YoungsModulusAndPoissonsRatio {
    double emodul;
    double nu;
  };

  ///<  Structure representing Young's modulus and shear modulus.
  struct YoungsModulusAndShearModulus {
    double emodul;
    double mu;
  };

  ///< Structure representing Young's modulus and bulk modulus.
  struct YoungsModulusAndBulkModulus {
    double emodul;
    double K;
  };

  ///< Structure representing Young's modulus and Lame's first parameter.
  struct YoungsModulusAndLamesFirstParameter {
    double emodul;
    double lambda;
  };

  ///< Structure representing bulk modulus and Lame's first parameter.
  struct BulkModulusAndLamesFirstParameter {
    double K;
    double lambda;
  };

  ///< Structure representing Lame's first parameter and shear modulus.
  struct LamesFirstParameterAndShearModulus {
    double lambda;
    double mu;
  };

  /**
   * \brief Concept for checking if a type is a valid material parameter tuple.
   *
   * \tparam MaterialParameter Type to check.
   */
  template <typename MaterialParameter>
  concept MaterialParameterTuple = std::is_same_v<MaterialParameter, YoungsModulusAndPoissonsRatio> or std::is_same_v<
      MaterialParameter, YoungsModulusAndBulkModulus> or std::is_same_v<MaterialParameter,
                                                                        YoungsModulusAndLamesFirstParameter> or std::
      is_same_v<MaterialParameter, BulkModulusAndLamesFirstParameter> or std::is_same_v<
          MaterialParameter, LamesFirstParameterAndShearModulus> or std::is_same_v<MaterialParameter,
                                                                                   YoungsModulusAndShearModulus>;

  /**
   * \brief Conversion utility for Lame's constants.
   *
   * \tparam ValuePair Type of the value pair to convert.
   */
  template <typename ValuePair>
  struct ConvertLameConstants {
    constexpr double toLamesFirstParameter() requires(
        !std::is_same_v<
            ValuePair,
            YoungsModulusAndLamesFirstParameter> and !std::is_same_v<ValuePair, BulkModulusAndLamesFirstParameter> and !std::is_same_v<ValuePair, LamesFirstParameterAndShearModulus>) {
      if constexpr (std::is_same_v<ValuePair, YoungsModulusAndPoissonsRatio>) {
        const auto& E  = vp.emodul;
        const auto& nu = vp.nu;
        return Dune::FloatCmp::eq(nu, 0.5) ? std::numeric_limits<double>::infinity()
                                           : E * nu / ((1.0 + nu) * (1.0 - 2.0 * nu));
      } else if constexpr (std::is_same_v<ValuePair, YoungsModulusAndShearModulus>) {
        const auto& E  = vp.emodul;
        const auto& mu = vp.mu;
        return mu * (E - 2.0 * mu) / (3.0 * mu - E);
      } else if constexpr (std::is_same_v<ValuePair, YoungsModulusAndBulkModulus>) {
        const auto& E = vp.emodul;
        const auto& K = vp.K;
        return 3.0 * K * (3.0 * K - E) / (9.0 * K - E);
      } else
        assert(false && "Your LameParameter request is not implemented");
    }

    constexpr double toBulkModulus() requires(
        !std::is_same_v<
            ValuePair, YoungsModulusAndBulkModulus> and !std::is_same_v<ValuePair, BulkModulusAndLamesFirstParameter>) {
      if constexpr (std::is_same_v<ValuePair, YoungsModulusAndPoissonsRatio>) {
        const auto& E  = vp.emodul;
        const auto& nu = vp.nu;
        return E / (3.0 * (1.0 - 2.0 * nu));
      } else if constexpr (std::is_same_v<ValuePair, YoungsModulusAndShearModulus>) {
        const auto& E  = vp.emodul;
        const auto& mu = vp.mu;
        return E * mu / (3.0 * (3.0 * mu - E));
      } else if constexpr (std::is_same_v<ValuePair, YoungsModulusAndLamesFirstParameter>) {
        const auto& E      = vp.emodul;
        const auto& lambda = vp.lambda;
        return (E + 3.0 * lambda + calcR(vp)) / 6.0;
      } else if constexpr (std::is_same_v<ValuePair, LamesFirstParameterAndShearModulus>) {
        const auto& lambda = vp.lambda;
        const auto& mu     = vp.mu;
        return lambda + 2.0 * mu / 3.0;
      } else
        assert(false && "Your LameParameter request is not implemented");
    }

    constexpr double toShearModulus() requires(
        !std::is_same_v<
            ValuePair,
            YoungsModulusAndShearModulus> and !std::is_same_v<ValuePair, LamesFirstParameterAndShearModulus>) {
      if constexpr (std::is_same_v<ValuePair, YoungsModulusAndPoissonsRatio>) {
        const auto& E  = vp.emodul;
        const auto& nu = vp.nu;
        return E / (2.0 * (1.0 + nu));
      } else if constexpr (std::is_same_v<ValuePair, YoungsModulusAndBulkModulus>) {
        const auto& E = vp.emodul;
        const auto& K = vp.K;
        return 3.0 * K * E / (9.0 * K - E);
      } else if constexpr (std::is_same_v<ValuePair, YoungsModulusAndLamesFirstParameter>) {
        const auto& E      = vp.emodul;
        const auto& lambda = vp.lambda;
        return (E - 3.0 * lambda + calcR(vp)) / 4.0;
      } else if constexpr (std::is_same_v<ValuePair, BulkModulusAndLamesFirstParameter>) {
        const auto& K      = vp.K;
        const auto& lambda = vp.lambda;
        return 3.0 * (K - lambda) / 2.0;
      } else
        assert(false && "Your LameParameter request is not implemented");
    }

    constexpr double toPWaveModulus() {
      if constexpr (std::is_same_v<ValuePair, YoungsModulusAndPoissonsRatio>) {
        const auto& E  = vp.emodul;
        const auto& nu = vp.nu;
        return E * (1.0 - nu) / ((1.0 + nu) * (1.0 - 2.0 * nu));
      } else if constexpr (std::is_same_v<ValuePair, YoungsModulusAndShearModulus>) {
        const auto& E  = vp.emodul;
        const auto& mu = vp.mu;
        return mu * (4.0 * mu - E) / (3.0 * mu - E);
      } else if constexpr (std::is_same_v<ValuePair, YoungsModulusAndBulkModulus>) {
        const auto& E = vp.emodul;
        const auto& K = vp.K;
        return 3.0 * K * (3.0 * K + E) / (9.0 * K - E);
      } else if constexpr (std::is_same_v<ValuePair, YoungsModulusAndLamesFirstParameter>) {
        const auto& E      = vp.emodul;
        const auto& lambda = vp.lambda;
        return (E - lambda + calcR(vp)) / 2.0;
      } else if constexpr (std::is_same_v<ValuePair, BulkModulusAndLamesFirstParameter>) {
        const auto& K      = vp.K;
        const auto& lambda = vp.lambda;
        return 3.0 * K - 2.0 * lambda;
      } else if constexpr (std::is_same_v<ValuePair, LamesFirstParameterAndShearModulus>) {
        const auto& lambda = vp.lambda;
        const auto& mu     = vp.mu;
        return lambda + 2.0 * mu;
      } else
        assert(false && "Your LameParameter request is not implemented");
    }

    constexpr double toPoissonsRatio() requires(!std::is_same_v<ValuePair, YoungsModulusAndPoissonsRatio>) {
      if constexpr (std::is_same_v<ValuePair, YoungsModulusAndShearModulus>) {
        const auto& E  = vp.emodul;
        const auto& mu = vp.mu;
        return E / (2.0 * mu) - 1.0;
      } else if constexpr (std::is_same_v<ValuePair, YoungsModulusAndBulkModulus>) {
        const auto& E = vp.emodul;
        const auto& K = vp.K;
        return (3.0 * K - E) / (6.0 * K);
      } else if constexpr (std::is_same_v<ValuePair, YoungsModulusAndLamesFirstParameter>) {
        const auto& E      = vp.emodul;
        const auto& lambda = vp.lambda;
        return 2.0 * lambda / (E + lambda + calcR(vp));
      } else if constexpr (std::is_same_v<ValuePair, BulkModulusAndLamesFirstParameter>) {
        const auto& K      = vp.K;
        const auto& lambda = vp.lambda;
        return lambda / (3 * K - lambda);
      } else if constexpr (std::is_same_v<ValuePair, LamesFirstParameterAndShearModulus>) {
        const auto& lambda = vp.lambda;
        const auto& mu     = vp.mu;
        return lambda / (2.0 * (lambda + mu));
      } else
        assert(false && "Your LameParameter request is not implemented");
    }

    constexpr double toYoungsModulus() requires(
        !std::is_same_v<
            ValuePair,
            YoungsModulusAndPoissonsRatio> and !std::is_same_v<ValuePair, YoungsModulusAndShearModulus> and !std::is_same_v<ValuePair, YoungsModulusAndBulkModulus> and !std::is_same_v<ValuePair, YoungsModulusAndLamesFirstParameter>) {
      if constexpr (std::is_same_v<ValuePair, BulkModulusAndLamesFirstParameter>) {
        return 9.0 * vp.K * (vp.K - vp.lambda) / (3.0 * vp.K - vp.lambda);
      } else if constexpr (std::is_same_v<ValuePair, LamesFirstParameterAndShearModulus>) {
        const auto& lambda = vp.lambda;
        const auto& mu     = vp.mu;
        return mu * (3.0 * lambda + 2.0 * mu) / (lambda + mu);
      } else
        assert(false && "Your LameParameter request is not implemented");
    }

  private : friend ConvertLameConstants<YoungsModulusAndPoissonsRatio> convertLameConstants(
                const YoungsModulusAndPoissonsRatio& p_vp);
    friend ConvertLameConstants<YoungsModulusAndShearModulus> convertLameConstants(
        const YoungsModulusAndShearModulus& p_vp);

    friend ConvertLameConstants<YoungsModulusAndBulkModulus> convertLameConstants(
        const YoungsModulusAndBulkModulus& p_vp);

    friend ConvertLameConstants<LamesFirstParameterAndShearModulus> convertLameConstants(
        const LamesFirstParameterAndShearModulus& p_vp);

    friend ConvertLameConstants<BulkModulusAndLamesFirstParameter> convertLameConstants(
        const BulkModulusAndLamesFirstParameter& p_vp);
    ConvertLameConstants(ValuePair&& p_vp) : vp(p_vp) {}
    ConvertLameConstants(const ValuePair& p_vp) : vp(p_vp) {}

    double calcR(const YoungsModulusAndLamesFirstParameter& vp_) {
      const auto& E      = vp_.emodul;
      const auto& lambda = vp_.lambda;
      return std::sqrt(E * E + 9 * lambda * lambda + 2 * E * lambda);
    }
    ValuePair vp;
  };
  inline ConvertLameConstants<YoungsModulusAndPoissonsRatio> convertLameConstants(
      const YoungsModulusAndPoissonsRatio& p_vp) {
    return {p_vp};
  }
  inline ConvertLameConstants<YoungsModulusAndShearModulus> convertLameConstants(
      const YoungsModulusAndShearModulus& p_vp) {
    return {p_vp};
  }
  inline ConvertLameConstants<YoungsModulusAndBulkModulus> convertLameConstants(
      const YoungsModulusAndBulkModulus& p_vp) {
    return {p_vp};
  }
  inline ConvertLameConstants<LamesFirstParameterAndShearModulus> convertLameConstants(
      const LamesFirstParameterAndShearModulus& p_vp) {
    return {p_vp};
  }
  inline ConvertLameConstants<BulkModulusAndLamesFirstParameter> convertLameConstants(
      const BulkModulusAndLamesFirstParameter& p_vp) {
    return {p_vp};
  }

  /**
   * \brief Converts Young's modulus and Poisson's ratio to Lame's first parameter and shear modulus.
   *
   * \param matParameter Young's modulus and Poisson's ratio.
   * \return Lame's first parameter and shear modulus.
   */
  inline auto toLamesFirstParameterAndShearModulus(const YoungsModulusAndPoissonsRatio& matParameter) {
    auto lambda = convertLameConstants(matParameter).toLamesFirstParameter();
    auto mu     = convertLameConstants(matParameter).toShearModulus();

    return LamesFirstParameterAndShearModulus{.lambda = lambda, .mu = mu};
  }

  /**
   * \brief Converts Lame's first parameter and shear modulus to Young's modulus and Poisson's ratio.
   *
   * \param matParameter Lame's first parameter and shear modulus.
   * \return Young's modulus and Poisson's ratio.
   */
  inline auto toYoungsModulusAndPoissonsRatio(const LamesFirstParameterAndShearModulus& matParameter) {
    auto emod = convertLameConstants(matParameter).toYoungsModulus();
    auto nu   = convertLameConstants(matParameter).toPoissonsRatio();

    return YoungsModulusAndPoissonsRatio{.emodul = emod, .nu = nu};
  }

}  // namespace Ikarus
