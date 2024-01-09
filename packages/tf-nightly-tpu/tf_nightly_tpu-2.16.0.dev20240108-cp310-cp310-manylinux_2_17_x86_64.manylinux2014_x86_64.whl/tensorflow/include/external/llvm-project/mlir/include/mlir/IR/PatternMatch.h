//===- PatternMatch.h - PatternMatcher classes -------==---------*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

#ifndef MLIR_IR_PATTERNMATCH_H
#define MLIR_IR_PATTERNMATCH_H

#include "mlir/IR/Builders.h"
#include "mlir/IR/BuiltinOps.h"
#include "llvm/ADT/FunctionExtras.h"
#include "llvm/Support/TypeName.h"
#include <optional>

namespace mlir {

class PatternRewriter;

//===----------------------------------------------------------------------===//
// PatternBenefit class
//===----------------------------------------------------------------------===//

/// This class represents the benefit of a pattern match in a unitless scheme
/// that ranges from 0 (very little benefit) to 65K.  The most common unit to
/// use here is the "number of operations matched" by the pattern.
///
/// This also has a sentinel representation that can be used for patterns that
/// fail to match.
///
class PatternBenefit {
  enum { ImpossibleToMatchSentinel = 65535 };

public:
  PatternBenefit() = default;
  PatternBenefit(unsigned benefit);
  PatternBenefit(const PatternBenefit &) = default;
  PatternBenefit &operator=(const PatternBenefit &) = default;

  static PatternBenefit impossibleToMatch() { return PatternBenefit(); }
  bool isImpossibleToMatch() const { return *this == impossibleToMatch(); }

  /// If the corresponding pattern can match, return its benefit.  If the
  // corresponding pattern isImpossibleToMatch() then this aborts.
  unsigned short getBenefit() const;

  bool operator==(const PatternBenefit &rhs) const {
    return representation == rhs.representation;
  }
  bool operator!=(const PatternBenefit &rhs) const { return !(*this == rhs); }
  bool operator<(const PatternBenefit &rhs) const {
    return representation < rhs.representation;
  }
  bool operator>(const PatternBenefit &rhs) const { return rhs < *this; }
  bool operator<=(const PatternBenefit &rhs) const { return !(*this > rhs); }
  bool operator>=(const PatternBenefit &rhs) const { return !(*this < rhs); }

private:
  unsigned short representation{ImpossibleToMatchSentinel};
};

//===----------------------------------------------------------------------===//
// Pattern
//===----------------------------------------------------------------------===//

/// This class contains all of the data related to a pattern, but does not
/// contain any methods or logic for the actual matching. This class is solely
/// used to interface with the metadata of a pattern, such as the benefit or
/// root operation.
class Pattern {
  /// This enum represents the kind of value used to select the root operations
  /// that match this pattern.
  enum class RootKind {
    /// The pattern root matches "any" operation.
    Any,
    /// The pattern root is matched using a concrete operation name.
    OperationName,
    /// The pattern root is matched using an interface ID.
    InterfaceID,
    /// The patter root is matched using a trait ID.
    TraitID
  };

public:
  /// Return a list of operations that may be generated when rewriting an
  /// operation instance with this pattern.
  ArrayRef<OperationName> getGeneratedOps() const { return generatedOps; }

  /// Return the root node that this pattern matches. Patterns that can match
  /// multiple root types return std::nullopt.
  std::optional<OperationName> getRootKind() const {
    if (rootKind == RootKind::OperationName)
      return OperationName::getFromOpaquePointer(rootValue);
    return std::nullopt;
  }

  /// Return the interface ID used to match the root operation of this pattern.
  /// If the pattern does not use an interface ID for deciding the root match,
  /// this returns std::nullopt.
  std::optional<TypeID> getRootInterfaceID() const {
    if (rootKind == RootKind::InterfaceID)
      return TypeID::getFromOpaquePointer(rootValue);
    return std::nullopt;
  }

  /// Return the trait ID used to match the root operation of this pattern.
  /// If the pattern does not use a trait ID for deciding the root match, this
  /// returns std::nullopt.
  std::optional<TypeID> getRootTraitID() const {
    if (rootKind == RootKind::TraitID)
      return TypeID::getFromOpaquePointer(rootValue);
    return std::nullopt;
  }

  /// Return the benefit (the inverse of "cost") of matching this pattern.  The
  /// benefit of a Pattern is always static - rewrites that may have dynamic
  /// benefit can be instantiated multiple times (different Pattern instances)
  /// for each benefit that they may return, and be guarded by different match
  /// condition predicates.
  PatternBenefit getBenefit() const { return benefit; }

  /// Returns true if this pattern is known to result in recursive application,
  /// i.e. this pattern may generate IR that also matches this pattern, but is
  /// known to bound the recursion. This signals to a rewrite driver that it is
  /// safe to apply this pattern recursively to generated IR.
  bool hasBoundedRewriteRecursion() const {
    return contextAndHasBoundedRecursion.getInt();
  }

  /// Return the MLIRContext used to create this pattern.
  MLIRContext *getContext() const {
    return contextAndHasBoundedRecursion.getPointer();
  }

  /// Return a readable name for this pattern. This name should only be used for
  /// debugging purposes, and may be empty.
  StringRef getDebugName() const { return debugName; }

  /// Set the human readable debug name used for this pattern. This name will
  /// only be used for debugging purposes.
  void setDebugName(StringRef name) { debugName = name; }

  /// Return the set of debug labels attached to this pattern.
  ArrayRef<StringRef> getDebugLabels() const { return debugLabels; }

  /// Add the provided debug labels to this pattern.
  void addDebugLabels(ArrayRef<StringRef> labels) {
    debugLabels.append(labels.begin(), labels.end());
  }
  void addDebugLabels(StringRef label) { debugLabels.push_back(label); }

protected:
  /// This class acts as a special tag that makes the desire to match "any"
  /// operation type explicit. This helps to avoid unnecessary usages of this
  /// feature, and ensures that the user is making a conscious decision.
  struct MatchAnyOpTypeTag {};
  /// This class acts as a special tag that makes the desire to match any
  /// operation that implements a given interface explicit. This helps to avoid
  /// unnecessary usages of this feature, and ensures that the user is making a
  /// conscious decision.
  struct MatchInterfaceOpTypeTag {};
  /// This class acts as a special tag that makes the desire to match any
  /// operation that implements a given trait explicit. This helps to avoid
  /// unnecessary usages of this feature, and ensures that the user is making a
  /// conscious decision.
  struct MatchTraitOpTypeTag {};

  /// Construct a pattern with a certain benefit that matches the operation
  /// with the given root name.
  Pattern(StringRef rootName, PatternBenefit benefit, MLIRContext *context,
          ArrayRef<StringRef> generatedNames = {});
  /// Construct a pattern that may match any operation type. `generatedNames`
  /// contains the names of operations that may be generated during a successful
  /// rewrite. `MatchAnyOpTypeTag` is just a tag to ensure that the "match any"
  /// behavior is what the user actually desired, `MatchAnyOpTypeTag()` should
  /// always be supplied here.
  Pattern(MatchAnyOpTypeTag tag, PatternBenefit benefit, MLIRContext *context,
          ArrayRef<StringRef> generatedNames = {});
  /// Construct a pattern that may match any operation that implements the
  /// interface defined by the provided `interfaceID`. `generatedNames` contains
  /// the names of operations that may be generated during a successful rewrite.
  /// `MatchInterfaceOpTypeTag` is just a tag to ensure that the "match
  /// interface" behavior is what the user actually desired,
  /// `MatchInterfaceOpTypeTag()` should always be supplied here.
  Pattern(MatchInterfaceOpTypeTag tag, TypeID interfaceID,
          PatternBenefit benefit, MLIRContext *context,
          ArrayRef<StringRef> generatedNames = {});
  /// Construct a pattern that may match any operation that implements the
  /// trait defined by the provided `traitID`. `generatedNames` contains the
  /// names of operations that may be generated during a successful rewrite.
  /// `MatchTraitOpTypeTag` is just a tag to ensure that the "match trait"
  /// behavior is what the user actually desired, `MatchTraitOpTypeTag()` should
  /// always be supplied here.
  Pattern(MatchTraitOpTypeTag tag, TypeID traitID, PatternBenefit benefit,
          MLIRContext *context, ArrayRef<StringRef> generatedNames = {});

  /// Set the flag detailing if this pattern has bounded rewrite recursion or
  /// not.
  void setHasBoundedRewriteRecursion(bool hasBoundedRecursionArg = true) {
    contextAndHasBoundedRecursion.setInt(hasBoundedRecursionArg);
  }

private:
  Pattern(const void *rootValue, RootKind rootKind,
          ArrayRef<StringRef> generatedNames, PatternBenefit benefit,
          MLIRContext *context);

  /// The value used to match the root operation of the pattern.
  const void *rootValue;
  RootKind rootKind;

  /// The expected benefit of matching this pattern.
  const PatternBenefit benefit;

  /// The context this pattern was created from, and a boolean flag indicating
  /// whether this pattern has bounded recursion or not.
  llvm::PointerIntPair<MLIRContext *, 1, bool> contextAndHasBoundedRecursion;

  /// A list of the potential operations that may be generated when rewriting
  /// an op with this pattern.
  SmallVector<OperationName, 2> generatedOps;

  /// A readable name for this pattern. May be empty.
  StringRef debugName;

  /// The set of debug labels attached to this pattern.
  SmallVector<StringRef, 0> debugLabels;
};

//===----------------------------------------------------------------------===//
// RewritePattern
//===----------------------------------------------------------------------===//

/// RewritePattern is the common base class for all DAG to DAG replacements.
/// There are two possible usages of this class:
///   * Multi-step RewritePattern with "match" and "rewrite"
///     - By overloading the "match" and "rewrite" functions, the user can
///       separate the concerns of matching and rewriting.
///   * Single-step RewritePattern with "matchAndRewrite"
///     - By overloading the "matchAndRewrite" function, the user can perform
///       the rewrite in the same call as the match.
///
class RewritePattern : public Pattern {
public:
  virtual ~RewritePattern() = default;

  /// Rewrite the IR rooted at the specified operation with the result of
  /// this pattern, generating any new operations with the specified
  /// builder.  If an unexpected error is encountered (an internal
  /// compiler error), it is emitted through the normal MLIR diagnostic
  /// hooks and the IR is left in a valid state.
  virtual void rewrite(Operation *op, PatternRewriter &rewriter) const;

  /// Attempt to match against code rooted at the specified operation,
  /// which is the same operation code as getRootKind().
  virtual LogicalResult match(Operation *op) const;

  /// Attempt to match against code rooted at the specified operation,
  /// which is the same operation code as getRootKind(). If successful, this
  /// function will automatically perform the rewrite.
  virtual LogicalResult matchAndRewrite(Operation *op,
                                        PatternRewriter &rewriter) const {
    if (succeeded(match(op))) {
      rewrite(op, rewriter);
      return success();
    }
    return failure();
  }

  /// This method provides a convenient interface for creating and initializing
  /// derived rewrite patterns of the given type `T`.
  template <typename T, typename... Args>
  static std::unique_ptr<T> create(Args &&...args) {
    std::unique_ptr<T> pattern =
        std::make_unique<T>(std::forward<Args>(args)...);
    initializePattern<T>(*pattern);

    // Set a default debug name if one wasn't provided.
    if (pattern->getDebugName().empty())
      pattern->setDebugName(llvm::getTypeName<T>());
    return pattern;
  }

protected:
  /// Inherit the base constructors from `Pattern`.
  using Pattern::Pattern;

private:
  /// Trait to check if T provides a `getOperationName` method.
  template <typename T, typename... Args>
  using has_initialize = decltype(std::declval<T>().initialize());
  template <typename T>
  using detect_has_initialize = llvm::is_detected<has_initialize, T>;

  /// Initialize the derived pattern by calling its `initialize` method.
  template <typename T>
  static std::enable_if_t<detect_has_initialize<T>::value>
  initializePattern(T &pattern) {
    pattern.initialize();
  }
  /// Empty derived pattern initializer for patterns that do not have an
  /// initialize method.
  template <typename T>
  static std::enable_if_t<!detect_has_initialize<T>::value>
  initializePattern(T &) {}

  /// An anchor for the virtual table.
  virtual void anchor();
};

namespace detail {
/// OpOrInterfaceRewritePatternBase is a wrapper around RewritePattern that
/// allows for matching and rewriting against an instance of a derived operation
/// class or Interface.
template <typename SourceOp>
struct OpOrInterfaceRewritePatternBase : public RewritePattern {
  using RewritePattern::RewritePattern;

  /// Wrappers around the RewritePattern methods that pass the derived op type.
  void rewrite(Operation *op, PatternRewriter &rewriter) const final {
    rewrite(cast<SourceOp>(op), rewriter);
  }
  LogicalResult match(Operation *op) const final {
    return match(cast<SourceOp>(op));
  }
  LogicalResult matchAndRewrite(Operation *op,
                                PatternRewriter &rewriter) const final {
    return matchAndRewrite(cast<SourceOp>(op), rewriter);
  }

  /// Rewrite and Match methods that operate on the SourceOp type. These must be
  /// overridden by the derived pattern class.
  virtual void rewrite(SourceOp op, PatternRewriter &rewriter) const {
    llvm_unreachable("must override rewrite or matchAndRewrite");
  }
  virtual LogicalResult match(SourceOp op) const {
    llvm_unreachable("must override match or matchAndRewrite");
  }
  virtual LogicalResult matchAndRewrite(SourceOp op,
                                        PatternRewriter &rewriter) const {
    if (succeeded(match(op))) {
      rewrite(op, rewriter);
      return success();
    }
    return failure();
  }
};
} // namespace detail

/// OpRewritePattern is a wrapper around RewritePattern that allows for
/// matching and rewriting against an instance of a derived operation class as
/// opposed to a raw Operation.
template <typename SourceOp>
struct OpRewritePattern
    : public detail::OpOrInterfaceRewritePatternBase<SourceOp> {
  /// Patterns must specify the root operation name they match against, and can
  /// also specify the benefit of the pattern matching and a list of generated
  /// ops.
  OpRewritePattern(MLIRContext *context, PatternBenefit benefit = 1,
                   ArrayRef<StringRef> generatedNames = {})
      : detail::OpOrInterfaceRewritePatternBase<SourceOp>(
            SourceOp::getOperationName(), benefit, context, generatedNames) {}
};

/// OpInterfaceRewritePattern is a wrapper around RewritePattern that allows for
/// matching and rewriting against an instance of an operation interface instead
/// of a raw Operation.
template <typename SourceOp>
struct OpInterfaceRewritePattern
    : public detail::OpOrInterfaceRewritePatternBase<SourceOp> {
  OpInterfaceRewritePattern(MLIRContext *context, PatternBenefit benefit = 1)
      : detail::OpOrInterfaceRewritePatternBase<SourceOp>(
            Pattern::MatchInterfaceOpTypeTag(), SourceOp::getInterfaceID(),
            benefit, context) {}
};

/// OpTraitRewritePattern is a wrapper around RewritePattern that allows for
/// matching and rewriting against instances of an operation that possess a
/// given trait.
template <template <typename> class TraitType>
class OpTraitRewritePattern : public RewritePattern {
public:
  OpTraitRewritePattern(MLIRContext *context, PatternBenefit benefit = 1)
      : RewritePattern(Pattern::MatchTraitOpTypeTag(), TypeID::get<TraitType>(),
                       benefit, context) {}
};

//===----------------------------------------------------------------------===//
// RewriterBase
//===----------------------------------------------------------------------===//

/// This class coordinates the application of a rewrite on a set of IR,
/// providing a way for clients to track mutations and create new operations.
/// This class serves as a common API for IR mutation between pattern rewrites
/// and non-pattern rewrites, and facilitates the development of shared
/// IR transformation utilities.
class RewriterBase : public OpBuilder {
public:
  struct Listener : public OpBuilder::Listener {
    Listener()
        : OpBuilder::Listener(ListenerBase::Kind::RewriterBaseListener) {}

    /// Notify the listener that the specified operation was modified in-place.
    virtual void notifyOperationModified(Operation *op) {}

    /// Notify the listener that the specified operation is about to be replaced
    /// with another operation. This is called before the uses of the old
    /// operation have been changed.
    ///
    /// By default, this function calls the "operation replaced with values"
    /// notification.
    virtual void notifyOperationReplaced(Operation *op,
                                         Operation *replacement) {
      notifyOperationReplaced(op, replacement->getResults());
    }

    /// Notify the listener that the specified operation is about to be replaced
    /// with the a range of values, potentially produced by other operations.
    /// This is called before the uses of the operation have been changed.
    virtual void notifyOperationReplaced(Operation *op,
                                         ValueRange replacement) {}

    /// Notify the listener that the specified operation is about to be erased.
    /// At this point, the operation has zero uses.
    virtual void notifyOperationRemoved(Operation *op) {}

    /// Notify the listener that the pattern failed to match the given
    /// operation, and provide a callback to populate a diagnostic with the
    /// reason why the failure occurred. This method allows for derived
    /// listeners to optionally hook into the reason why a rewrite failed, and
    /// display it to users.
    virtual LogicalResult
    notifyMatchFailure(Location loc,
                       function_ref<void(Diagnostic &)> reasonCallback) {
      return failure();
    }

    static bool classof(const OpBuilder::Listener *base);
  };

  /// A listener that forwards all notifications to another listener. This
  /// struct can be used as a base to create listener chains, so that multiple
  /// listeners can be notified of IR changes.
  struct ForwardingListener : public RewriterBase::Listener {
    ForwardingListener(OpBuilder::Listener *listener) : listener(listener) {}

    void notifyOperationInserted(Operation *op) override {
      listener->notifyOperationInserted(op);
    }
    void notifyBlockCreated(Block *block) override {
      listener->notifyBlockCreated(block);
    }
    void notifyOperationModified(Operation *op) override {
      if (auto *rewriteListener = dyn_cast<RewriterBase::Listener>(listener))
        rewriteListener->notifyOperationModified(op);
    }
    void notifyOperationReplaced(Operation *op, Operation *newOp) override {
      if (auto *rewriteListener = dyn_cast<RewriterBase::Listener>(listener))
        rewriteListener->notifyOperationReplaced(op, newOp);
    }
    void notifyOperationReplaced(Operation *op,
                                 ValueRange replacement) override {
      if (auto *rewriteListener = dyn_cast<RewriterBase::Listener>(listener))
        rewriteListener->notifyOperationReplaced(op, replacement);
    }
    void notifyOperationRemoved(Operation *op) override {
      if (auto *rewriteListener = dyn_cast<RewriterBase::Listener>(listener))
        rewriteListener->notifyOperationRemoved(op);
    }
    LogicalResult notifyMatchFailure(
        Location loc,
        function_ref<void(Diagnostic &)> reasonCallback) override {
      if (auto *rewriteListener = dyn_cast<RewriterBase::Listener>(listener))
        return rewriteListener->notifyMatchFailure(loc, reasonCallback);
      return failure();
    }

  private:
    OpBuilder::Listener *listener;
  };

  /// Move the blocks that belong to "region" before the given position in
  /// another region "parent". The two regions must be different. The caller
  /// is responsible for creating or updating the operation transferring flow
  /// of control to the region and passing it the correct block arguments.
  virtual void inlineRegionBefore(Region &region, Region &parent,
                                  Region::iterator before);
  void inlineRegionBefore(Region &region, Block *before);

  /// Clone the blocks that belong to "region" before the given position in
  /// another region "parent". The two regions must be different. The caller is
  /// responsible for creating or updating the operation transferring flow of
  /// control to the region and passing it the correct block arguments.
  virtual void cloneRegionBefore(Region &region, Region &parent,
                                 Region::iterator before, IRMapping &mapping);
  void cloneRegionBefore(Region &region, Region &parent,
                         Region::iterator before);
  void cloneRegionBefore(Region &region, Block *before);

  /// This method replaces the uses of the results of `op` with the values in
  /// `newValues` when the provided `functor` returns true for a specific use.
  /// The number of values in `newValues` is required to match the number of
  /// results of `op`. `allUsesReplaced`, if non-null, is set to true if all of
  /// the uses of `op` were replaced. Note that in some rewriters, the given
  /// 'functor' may be stored beyond the lifetime of the rewrite being applied.
  /// As such, the function should not capture by reference and instead use
  /// value capture as necessary.
  virtual void
  replaceOpWithIf(Operation *op, ValueRange newValues, bool *allUsesReplaced,
                  llvm::unique_function<bool(OpOperand &) const> functor);
  void replaceOpWithIf(Operation *op, ValueRange newValues,
                       llvm::unique_function<bool(OpOperand &) const> functor) {
    replaceOpWithIf(op, newValues, /*allUsesReplaced=*/nullptr,
                    std::move(functor));
  }

  /// This method replaces the uses of the results of `op` with the values in
  /// `newValues` when a use is nested within the given `block`. The number of
  /// values in `newValues` is required to match the number of results of `op`.
  /// If all uses of this operation are replaced, the operation is erased.
  void replaceOpWithinBlock(Operation *op, ValueRange newValues, Block *block,
                            bool *allUsesReplaced = nullptr);

  /// This method replaces the results of the operation with the specified list
  /// of values. The number of provided values must match the number of results
  /// of the operation. The replaced op is erased.
  virtual void replaceOp(Operation *op, ValueRange newValues);

  /// This method replaces the results of the operation with the specified
  /// new op (replacement). The number of results of the two operations must
  /// match. The replaced op is erased.
  virtual void replaceOp(Operation *op, Operation *newOp);

  /// Replaces the result op with a new op that is created without verification.
  /// The result values of the two ops must be the same types.
  template <typename OpTy, typename... Args>
  OpTy replaceOpWithNewOp(Operation *op, Args &&...args) {
    auto newOp = create<OpTy>(op->getLoc(), std::forward<Args>(args)...);
    replaceOp(op, newOp.getOperation());
    return newOp;
  }

  /// This method erases an operation that is known to have no uses.
  virtual void eraseOp(Operation *op);

  /// This method erases all operations in a block.
  virtual void eraseBlock(Block *block);

  /// Inline the operations of block 'source' into block 'dest' before the given
  /// position. The source block will be deleted and must have no uses.
  /// 'argValues' is used to replace the block arguments of 'source'.
  ///
  /// If the source block is inserted at the end of the dest block, the dest
  /// block must have no successors. Similarly, if the source block is inserted
  /// somewhere in the middle (or beginning) of the dest block, the source block
  /// must have no successors. Otherwise, the resulting IR would have
  /// unreachable operations.
  virtual void inlineBlockBefore(Block *source, Block *dest,
                                 Block::iterator before,
                                 ValueRange argValues = std::nullopt);

  /// Inline the operations of block 'source' before the operation 'op'. The
  /// source block will be deleted and must have no uses. 'argValues' is used to
  /// replace the block arguments of 'source'
  ///
  /// The source block must have no successors. Otherwise, the resulting IR
  /// would have unreachable operations.
  void inlineBlockBefore(Block *source, Operation *op,
                         ValueRange argValues = std::nullopt);

  /// Inline the operations of block 'source' into the end of block 'dest'. The
  /// source block will be deleted and must have no uses. 'argValues' is used to
  /// replace the block arguments of 'source'
  ///
  /// The dest block must have no successors. Otherwise, the resulting IR would
  /// have unreachable operation.
  void mergeBlocks(Block *source, Block *dest,
                   ValueRange argValues = std::nullopt);

  /// Split the operations starting at "before" (inclusive) out of the given
  /// block into a new block, and return it.
  virtual Block *splitBlock(Block *block, Block::iterator before);

  /// This method is used to notify the rewriter that an in-place operation
  /// modification is about to happen. A call to this function *must* be
  /// followed by a call to either `finalizeRootUpdate` or `cancelRootUpdate`.
  /// This is a minor efficiency win (it avoids creating a new operation and
  /// removing the old one) but also often allows simpler code in the client.
  virtual void startRootUpdate(Operation *op) {}

  /// This method is used to signal the end of a root update on the given
  /// operation. This can only be called on operations that were provided to a
  /// call to `startRootUpdate`.
  virtual void finalizeRootUpdate(Operation *op);

  /// This method cancels a pending root update. This can only be called on
  /// operations that were provided to a call to `startRootUpdate`.
  virtual void cancelRootUpdate(Operation *op) {}

  /// This method is a utility wrapper around a root update of an operation. It
  /// wraps calls to `startRootUpdate` and `finalizeRootUpdate` around the given
  /// callable.
  template <typename CallableT>
  void updateRootInPlace(Operation *root, CallableT &&callable) {
    startRootUpdate(root);
    callable();
    finalizeRootUpdate(root);
  }

  /// Find uses of `from` and replace them with `to`. It also marks every
  /// modified uses and notifies the rewriter that an in-place operation
  /// modification is about to happen.
  void replaceAllUsesWith(Value from, Value to) {
    return replaceAllUsesWith(from.getImpl(), to);
  }
  template <typename OperandType, typename ValueT>
  void replaceAllUsesWith(IRObjectWithUseList<OperandType> *from, ValueT &&to) {
    for (OperandType &operand : llvm::make_early_inc_range(from->getUses())) {
      Operation *op = operand.getOwner();
      updateRootInPlace(op, [&]() { operand.set(to); });
    }
  }
  void replaceAllUsesWith(ValueRange from, ValueRange to) {
    assert(from.size() == to.size() && "incorrect number of replacements");
    for (auto it : llvm::zip(from, to))
      replaceAllUsesWith(std::get<0>(it), std::get<1>(it));
  }

  /// Find uses of `from` and replace them with `to` if the `functor` returns
  /// true. It also marks every modified uses and notifies the rewriter that an
  /// in-place operation modification is about to happen.
  void replaceUsesWithIf(Value from, Value to,
                         function_ref<bool(OpOperand &)> functor);
  void replaceUsesWithIf(ValueRange from, ValueRange to,
                         function_ref<bool(OpOperand &)> functor) {
    assert(from.size() == to.size() && "incorrect number of replacements");
    for (auto it : llvm::zip(from, to))
      replaceUsesWithIf(std::get<0>(it), std::get<1>(it), functor);
  }

  /// Find uses of `from` and replace them with `to` except if the user is
  /// `exceptedUser`. It also marks every modified uses and notifies the
  /// rewriter that an in-place operation modification is about to happen.
  void replaceAllUsesExcept(Value from, Value to, Operation *exceptedUser) {
    return replaceUsesWithIf(from, to, [&](OpOperand &use) {
      Operation *user = use.getOwner();
      return user != exceptedUser;
    });
  }

  /// Used to notify the rewriter that the IR failed to be rewritten because of
  /// a match failure, and provide a callback to populate a diagnostic with the
  /// reason why the failure occurred. This method allows for derived rewriters
  /// to optionally hook into the reason why a rewrite failed, and display it to
  /// users.
  template <typename CallbackT>
  std::enable_if_t<!std::is_convertible<CallbackT, Twine>::value, LogicalResult>
  notifyMatchFailure(Location loc, CallbackT &&reasonCallback) {
#ifndef NDEBUG
    if (auto *rewriteListener = dyn_cast_if_present<Listener>(listener))
      return rewriteListener->notifyMatchFailure(
          loc, function_ref<void(Diagnostic &)>(reasonCallback));
    return failure();
#else
    return failure();
#endif
  }
  template <typename CallbackT>
  std::enable_if_t<!std::is_convertible<CallbackT, Twine>::value, LogicalResult>
  notifyMatchFailure(Operation *op, CallbackT &&reasonCallback) {
    if (auto *rewriteListener = dyn_cast_if_present<Listener>(listener))
      return rewriteListener->notifyMatchFailure(
          op->getLoc(), function_ref<void(Diagnostic &)>(reasonCallback));
    return failure();
  }
  template <typename ArgT>
  LogicalResult notifyMatchFailure(ArgT &&arg, const Twine &msg) {
    return notifyMatchFailure(std::forward<ArgT>(arg),
                              [&](Diagnostic &diag) { diag << msg; });
  }
  template <typename ArgT>
  LogicalResult notifyMatchFailure(ArgT &&arg, const char *msg) {
    return notifyMatchFailure(std::forward<ArgT>(arg), Twine(msg));
  }

protected:
  /// Initialize the builder.
  explicit RewriterBase(MLIRContext *ctx,
                        OpBuilder::Listener *listener = nullptr)
      : OpBuilder(ctx, listener) {}
  explicit RewriterBase(const OpBuilder &otherBuilder)
      : OpBuilder(otherBuilder) {}
  virtual ~RewriterBase();

private:
  void operator=(const RewriterBase &) = delete;
  RewriterBase(const RewriterBase &) = delete;
};

//===----------------------------------------------------------------------===//
// IRRewriter
//===----------------------------------------------------------------------===//

/// This class coordinates rewriting a piece of IR outside of a pattern rewrite,
/// providing a way to keep track of the mutations made to the IR. This class
/// should only be used in situations where another `RewriterBase` instance,
/// such as a `PatternRewriter`, is not available.
class IRRewriter : public RewriterBase {
public:
  explicit IRRewriter(MLIRContext *ctx, OpBuilder::Listener *listener = nullptr)
      : RewriterBase(ctx, listener) {}
  explicit IRRewriter(const OpBuilder &builder) : RewriterBase(builder) {}
};

//===----------------------------------------------------------------------===//
// PatternRewriter
//===----------------------------------------------------------------------===//

/// A special type of `RewriterBase` that coordinates the application of a
/// rewrite pattern on the current IR being matched, providing a way to keep
/// track of any mutations made. This class should be used to perform all
/// necessary IR mutations within a rewrite pattern, as the pattern driver may
/// be tracking various state that would be invalidated when a mutation takes
/// place.
class PatternRewriter : public RewriterBase {
public:
  using RewriterBase::RewriterBase;

  /// A hook used to indicate if the pattern rewriter can recover from failure
  /// during the rewrite stage of a pattern. For example, if the pattern
  /// rewriter supports rollback, it may progress smoothly even if IR was
  /// changed during the rewrite.
  virtual bool canRecoverFromRewriteFailure() const { return false; }
};

} // namespace mlir

// Optionally expose PDL pattern matching methods.
#include "PDLPatternMatch.h.inc"

namespace mlir {

//===----------------------------------------------------------------------===//
// RewritePatternSet
//===----------------------------------------------------------------------===//

class RewritePatternSet {
  using NativePatternListT = std::vector<std::unique_ptr<RewritePattern>>;

public:
  RewritePatternSet(MLIRContext *context) : context(context) {}

  /// Construct a RewritePatternSet populated with the given pattern.
  RewritePatternSet(MLIRContext *context,
                    std::unique_ptr<RewritePattern> pattern)
      : context(context) {
    nativePatterns.emplace_back(std::move(pattern));
  }
  RewritePatternSet(PDLPatternModule &&pattern)
      : context(pattern.getContext()), pdlPatterns(std::move(pattern)) {}

  MLIRContext *getContext() const { return context; }

  /// Return the native patterns held in this list.
  NativePatternListT &getNativePatterns() { return nativePatterns; }

  /// Return the PDL patterns held in this list.
  PDLPatternModule &getPDLPatterns() { return pdlPatterns; }

  /// Clear out all of the held patterns in this list.
  void clear() {
    nativePatterns.clear();
    pdlPatterns.clear();
  }

  //===--------------------------------------------------------------------===//
  // 'add' methods for adding patterns to the set.
  //===--------------------------------------------------------------------===//

  /// Add an instance of each of the pattern types 'Ts' to the pattern list with
  /// the given arguments. Return a reference to `this` for chaining insertions.
  /// Note: ConstructorArg is necessary here to separate the two variadic lists.
  template <typename... Ts, typename ConstructorArg,
            typename... ConstructorArgs,
            typename = std::enable_if_t<sizeof...(Ts) != 0>>
  RewritePatternSet &add(ConstructorArg &&arg, ConstructorArgs &&...args) {
    // The following expands a call to emplace_back for each of the pattern
    // types 'Ts'.
    (addImpl<Ts>(/*debugLabels=*/std::nullopt,
                 std::forward<ConstructorArg>(arg),
                 std::forward<ConstructorArgs>(args)...),
     ...);
    return *this;
  }
  /// An overload of the above `add` method that allows for attaching a set
  /// of debug labels to the attached patterns. This is useful for labeling
  /// groups of patterns that may be shared between multiple different
  /// passes/users.
  template <typename... Ts, typename ConstructorArg,
            typename... ConstructorArgs,
            typename = std::enable_if_t<sizeof...(Ts) != 0>>
  RewritePatternSet &addWithLabel(ArrayRef<StringRef> debugLabels,
                                  ConstructorArg &&arg,
                                  ConstructorArgs &&...args) {
    // The following expands a call to emplace_back for each of the pattern
    // types 'Ts'.
    (addImpl<Ts>(debugLabels, arg, args...), ...);
    return *this;
  }

  /// Add an instance of each of the pattern types 'Ts'. Return a reference to
  /// `this` for chaining insertions.
  template <typename... Ts>
  RewritePatternSet &add() {
    (addImpl<Ts>(), ...);
    return *this;
  }

  /// Add the given native pattern to the pattern list. Return a reference to
  /// `this` for chaining insertions.
  RewritePatternSet &add(std::unique_ptr<RewritePattern> pattern) {
    nativePatterns.emplace_back(std::move(pattern));
    return *this;
  }

  /// Add the given PDL pattern to the pattern list. Return a reference to
  /// `this` for chaining insertions.
  RewritePatternSet &add(PDLPatternModule &&pattern) {
    pdlPatterns.mergeIn(std::move(pattern));
    return *this;
  }

  // Add a matchAndRewrite style pattern represented as a C function pointer.
  template <typename OpType>
  RewritePatternSet &
  add(LogicalResult (*implFn)(OpType, PatternRewriter &rewriter),
      PatternBenefit benefit = 1, ArrayRef<StringRef> generatedNames = {}) {
    struct FnPattern final : public OpRewritePattern<OpType> {
      FnPattern(LogicalResult (*implFn)(OpType, PatternRewriter &rewriter),
                MLIRContext *context, PatternBenefit benefit,
                ArrayRef<StringRef> generatedNames)
          : OpRewritePattern<OpType>(context, benefit, generatedNames),
            implFn(implFn) {}

      LogicalResult matchAndRewrite(OpType op,
                                    PatternRewriter &rewriter) const override {
        return implFn(op, rewriter);
      }

    private:
      LogicalResult (*implFn)(OpType, PatternRewriter &rewriter);
    };
    add(std::make_unique<FnPattern>(std::move(implFn), getContext(), benefit,
                                    generatedNames));
    return *this;
  }

  //===--------------------------------------------------------------------===//
  // Pattern Insertion
  //===--------------------------------------------------------------------===//

  // TODO: These are soft deprecated in favor of the 'add' methods above.

  /// Add an instance of each of the pattern types 'Ts' to the pattern list with
  /// the given arguments. Return a reference to `this` for chaining insertions.
  /// Note: ConstructorArg is necessary here to separate the two variadic lists.
  template <typename... Ts, typename ConstructorArg,
            typename... ConstructorArgs,
            typename = std::enable_if_t<sizeof...(Ts) != 0>>
  RewritePatternSet &insert(ConstructorArg &&arg, ConstructorArgs &&...args) {
    // The following expands a call to emplace_back for each of the pattern
    // types 'Ts'.
    (addImpl<Ts>(/*debugLabels=*/std::nullopt, arg, args...), ...);
    return *this;
  }

  /// Add an instance of each of the pattern types 'Ts'. Return a reference to
  /// `this` for chaining insertions.
  template <typename... Ts>
  RewritePatternSet &insert() {
    (addImpl<Ts>(), ...);
    return *this;
  }

  /// Add the given native pattern to the pattern list. Return a reference to
  /// `this` for chaining insertions.
  RewritePatternSet &insert(std::unique_ptr<RewritePattern> pattern) {
    nativePatterns.emplace_back(std::move(pattern));
    return *this;
  }

  /// Add the given PDL pattern to the pattern list. Return a reference to
  /// `this` for chaining insertions.
  RewritePatternSet &insert(PDLPatternModule &&pattern) {
    pdlPatterns.mergeIn(std::move(pattern));
    return *this;
  }

  // Add a matchAndRewrite style pattern represented as a C function pointer.
  template <typename OpType>
  RewritePatternSet &
  insert(LogicalResult (*implFn)(OpType, PatternRewriter &rewriter)) {
    struct FnPattern final : public OpRewritePattern<OpType> {
      FnPattern(LogicalResult (*implFn)(OpType, PatternRewriter &rewriter),
                MLIRContext *context)
          : OpRewritePattern<OpType>(context), implFn(implFn) {
        this->setDebugName(llvm::getTypeName<FnPattern>());
      }

      LogicalResult matchAndRewrite(OpType op,
                                    PatternRewriter &rewriter) const override {
        return implFn(op, rewriter);
      }

    private:
      LogicalResult (*implFn)(OpType, PatternRewriter &rewriter);
    };
    add(std::make_unique<FnPattern>(std::move(implFn), getContext()));
    return *this;
  }

private:
  /// Add an instance of the pattern type 'T'. Return a reference to `this` for
  /// chaining insertions.
  template <typename T, typename... Args>
  std::enable_if_t<std::is_base_of<RewritePattern, T>::value>
  addImpl(ArrayRef<StringRef> debugLabels, Args &&...args) {
    std::unique_ptr<T> pattern =
        RewritePattern::create<T>(std::forward<Args>(args)...);
    pattern->addDebugLabels(debugLabels);
    nativePatterns.emplace_back(std::move(pattern));
  }

  template <typename T, typename... Args>
  std::enable_if_t<std::is_base_of<PDLPatternModule, T>::value>
  addImpl(ArrayRef<StringRef> debugLabels, Args &&...args) {
    // TODO: Add the provided labels to the PDL pattern when PDL supports
    // labels.
    pdlPatterns.mergeIn(T(std::forward<Args>(args)...));
  }

  MLIRContext *const context;
  NativePatternListT nativePatterns;

  // Patterns expressed with PDL. This will compile to a stub class when PDL is
  // not enabled.
  PDLPatternModule pdlPatterns;
};

} // namespace mlir

#endif // MLIR_IR_PATTERNMATCH_H
