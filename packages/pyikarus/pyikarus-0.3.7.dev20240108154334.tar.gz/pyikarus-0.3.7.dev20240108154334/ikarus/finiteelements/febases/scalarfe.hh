// SPDX-FileCopyrightText: 2021-2024 The Ikarus Developers mueller@ibb.uni-stuttgart.de
// SPDX-License-Identifier: LGPL-3.0-or-later

/**
 * @file scalarFE.hh
 * @brief Contains the ScalarFieldFE class, a class for Single-DOF elements using a scalar basis.
 */

#pragma once

#include <ikarus/finiteelements/fetraits.hh>

namespace Ikarus {

  /**
   * @brief ScalarFieldFE class, a class for Single-DOF elements using a scalar basis.
   *
   * @tparam Basis_ Type of the scalar basis.
   */
  template <typename Basis_>
  class ScalarFieldFE {
  public:
    using Basis                   = Basis_;                          ///< Type of the root basis.
    using LocalView               = typename Basis::LocalView;       ///< Type of the local view.
    using GlobalIndex             = typename LocalView::MultiIndex;  ///< Type of the global index.
    using GridElement             = typename LocalView::Element;     ///< Type of the grid element.
    using Traits                  = FETraits<GridElement>;           ///< Type of the traits.
    static constexpr int worlddim = Traits::worlddim;                ///< Dimension of the world space.
    /**
     * @brief Constructor for the ScalarFieldFE class.
     *
     * @param basis The scalar basis.
     * @param element The local element.
     */
    explicit ScalarFieldFE(const Basis& basis, const typename LocalView::Element& element)
        : localView_{basis.localView()} {
      static_assert(Basis::PreBasis::Node::CHILDREN == 0, "This is no scalar basis!");
      localView_.bind(element);
    }

    /**
     * @brief Get the size of the finite element.
     *
     * @return The size of the finite element.
     */
    [[nodiscard]] int size() const { return localView_.size(); }

    /**
     * @brief Get the global flat indices of the finite element.
     *
     * @param globalIndices Vector to store global flat indices.
     */
    void globalFlatIndices(std::vector<GlobalIndex>& globalIndices) const {
      const auto& fe = localView_.tree().finiteElement();
      for (size_t i = 0; i < fe.size(); ++i)
        globalIndices.push_back(localView_.index(localView_.tree().localIndex(i)));
    }

    /**
     * @brief Get the entity associated with the finite element.
     *
     * @return The entity associated with the finite element.
     */
    const GridElement& gridElement() const { return localView_.element(); }

    /**
     * @brief Get the local view of the finite element.
     *
     * @return The local view of the finite element.
     */
    const LocalView& localView() const { return localView_; }

    /**
     * @brief Get the local view of the finite element.
     *
     * @return The local view of the finite element.
     */
    LocalView& localView() { return localView_; }

  private:
    LocalView localView_; /**< Local view of the finite element. */
  };
}  // namespace Ikarus
