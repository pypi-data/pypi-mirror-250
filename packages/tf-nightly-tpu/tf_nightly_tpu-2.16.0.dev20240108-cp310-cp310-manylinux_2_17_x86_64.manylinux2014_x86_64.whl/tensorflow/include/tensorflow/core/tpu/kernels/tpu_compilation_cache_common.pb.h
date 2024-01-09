// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/core/tpu/kernels/tpu_compilation_cache_common.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2ftpu_2fkernels_2ftpu_5fcompilation_5fcache_5fcommon_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2ftpu_2fkernels_2ftpu_5fcompilation_5fcache_5fcommon_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3021000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3021009 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/generated_enum_reflection.h>
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2fcore_2ftpu_2fkernels_2ftpu_5fcompilation_5fcache_5fcommon_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_tensorflow_2fcore_2ftpu_2fkernels_2ftpu_5fcompilation_5fcache_5fcommon_2eproto {
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2fcore_2ftpu_2fkernels_2ftpu_5fcompilation_5fcache_5fcommon_2eproto;
namespace tensorflow {
namespace tpu {
class GetTpuProgramRequest;
struct GetTpuProgramRequestDefaultTypeInternal;
extern GetTpuProgramRequestDefaultTypeInternal _GetTpuProgramRequest_default_instance_;
class TpuCompilationUidAndIndex;
struct TpuCompilationUidAndIndexDefaultTypeInternal;
extern TpuCompilationUidAndIndexDefaultTypeInternal _TpuCompilationUidAndIndex_default_instance_;
}  // namespace tpu
}  // namespace tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> ::tensorflow::tpu::GetTpuProgramRequest* Arena::CreateMaybeMessage<::tensorflow::tpu::GetTpuProgramRequest>(Arena*);
template<> ::tensorflow::tpu::TpuCompilationUidAndIndex* Arena::CreateMaybeMessage<::tensorflow::tpu::TpuCompilationUidAndIndex>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace tensorflow {
namespace tpu {

enum CompilationCacheFetchTarget : int {
  INVALID = 0,
  MAIN = 1,
  SHARDING = 2,
  UNSHARDING = 3,
  CompilationCacheFetchTarget_INT_MIN_SENTINEL_DO_NOT_USE_ = std::numeric_limits<int32_t>::min(),
  CompilationCacheFetchTarget_INT_MAX_SENTINEL_DO_NOT_USE_ = std::numeric_limits<int32_t>::max()
};
bool CompilationCacheFetchTarget_IsValid(int value);
constexpr CompilationCacheFetchTarget CompilationCacheFetchTarget_MIN = INVALID;
constexpr CompilationCacheFetchTarget CompilationCacheFetchTarget_MAX = UNSHARDING;
constexpr int CompilationCacheFetchTarget_ARRAYSIZE = CompilationCacheFetchTarget_MAX + 1;

const ::PROTOBUF_NAMESPACE_ID::EnumDescriptor* CompilationCacheFetchTarget_descriptor();
template<typename T>
inline const std::string& CompilationCacheFetchTarget_Name(T enum_t_value) {
  static_assert(::std::is_same<T, CompilationCacheFetchTarget>::value ||
    ::std::is_integral<T>::value,
    "Incorrect type passed to function CompilationCacheFetchTarget_Name.");
  return ::PROTOBUF_NAMESPACE_ID::internal::NameOfEnum(
    CompilationCacheFetchTarget_descriptor(), enum_t_value);
}
inline bool CompilationCacheFetchTarget_Parse(
    ::PROTOBUF_NAMESPACE_ID::ConstStringParam name, CompilationCacheFetchTarget* value) {
  return ::PROTOBUF_NAMESPACE_ID::internal::ParseNamedEnum<CompilationCacheFetchTarget>(
    CompilationCacheFetchTarget_descriptor(), name, value);
}
// ===================================================================

class TpuCompilationUidAndIndex final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.tpu.TpuCompilationUidAndIndex) */ {
 public:
  inline TpuCompilationUidAndIndex() : TpuCompilationUidAndIndex(nullptr) {}
  ~TpuCompilationUidAndIndex() override;
  explicit PROTOBUF_CONSTEXPR TpuCompilationUidAndIndex(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  TpuCompilationUidAndIndex(const TpuCompilationUidAndIndex& from);
  TpuCompilationUidAndIndex(TpuCompilationUidAndIndex&& from) noexcept
    : TpuCompilationUidAndIndex() {
    *this = ::std::move(from);
  }

  inline TpuCompilationUidAndIndex& operator=(const TpuCompilationUidAndIndex& from) {
    CopyFrom(from);
    return *this;
  }
  inline TpuCompilationUidAndIndex& operator=(TpuCompilationUidAndIndex&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const TpuCompilationUidAndIndex& default_instance() {
    return *internal_default_instance();
  }
  static inline const TpuCompilationUidAndIndex* internal_default_instance() {
    return reinterpret_cast<const TpuCompilationUidAndIndex*>(
               &_TpuCompilationUidAndIndex_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(TpuCompilationUidAndIndex& a, TpuCompilationUidAndIndex& b) {
    a.Swap(&b);
  }
  inline void Swap(TpuCompilationUidAndIndex* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(TpuCompilationUidAndIndex* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  TpuCompilationUidAndIndex* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<TpuCompilationUidAndIndex>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const TpuCompilationUidAndIndex& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const TpuCompilationUidAndIndex& from) {
    TpuCompilationUidAndIndex::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(TpuCompilationUidAndIndex* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.tpu.TpuCompilationUidAndIndex";
  }
  protected:
  explicit TpuCompilationUidAndIndex(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kUidFieldNumber = 1,
    kProtoIndexFieldNumber = 2,
  };
  // int64 uid = 1;
  void clear_uid();
  int64_t uid() const;
  void set_uid(int64_t value);
  private:
  int64_t _internal_uid() const;
  void _internal_set_uid(int64_t value);
  public:

  // int32 proto_index = 2;
  void clear_proto_index();
  int32_t proto_index() const;
  void set_proto_index(int32_t value);
  private:
  int32_t _internal_proto_index() const;
  void _internal_set_proto_index(int32_t value);
  public:

  // @@protoc_insertion_point(class_scope:tensorflow.tpu.TpuCompilationUidAndIndex)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    int64_t uid_;
    int32_t proto_index_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2fcore_2ftpu_2fkernels_2ftpu_5fcompilation_5fcache_5fcommon_2eproto;
};
// -------------------------------------------------------------------

class GetTpuProgramRequest final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.tpu.GetTpuProgramRequest) */ {
 public:
  inline GetTpuProgramRequest() : GetTpuProgramRequest(nullptr) {}
  ~GetTpuProgramRequest() override;
  explicit PROTOBUF_CONSTEXPR GetTpuProgramRequest(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  GetTpuProgramRequest(const GetTpuProgramRequest& from);
  GetTpuProgramRequest(GetTpuProgramRequest&& from) noexcept
    : GetTpuProgramRequest() {
    *this = ::std::move(from);
  }

  inline GetTpuProgramRequest& operator=(const GetTpuProgramRequest& from) {
    CopyFrom(from);
    return *this;
  }
  inline GetTpuProgramRequest& operator=(GetTpuProgramRequest&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const GetTpuProgramRequest& default_instance() {
    return *internal_default_instance();
  }
  enum KeyOneofCase {
    kKey = 1,
    kUidAndIndex = 2,
    KEY_ONEOF_NOT_SET = 0,
  };

  static inline const GetTpuProgramRequest* internal_default_instance() {
    return reinterpret_cast<const GetTpuProgramRequest*>(
               &_GetTpuProgramRequest_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  friend void swap(GetTpuProgramRequest& a, GetTpuProgramRequest& b) {
    a.Swap(&b);
  }
  inline void Swap(GetTpuProgramRequest* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(GetTpuProgramRequest* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  GetTpuProgramRequest* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<GetTpuProgramRequest>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const GetTpuProgramRequest& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const GetTpuProgramRequest& from) {
    GetTpuProgramRequest::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(GetTpuProgramRequest* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.tpu.GetTpuProgramRequest";
  }
  protected:
  explicit GetTpuProgramRequest(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kFetchTargetFieldNumber = 3,
    kKeyFieldNumber = 1,
    kUidAndIndexFieldNumber = 2,
  };
  // .tensorflow.tpu.CompilationCacheFetchTarget fetch_target = 3;
  void clear_fetch_target();
  ::tensorflow::tpu::CompilationCacheFetchTarget fetch_target() const;
  void set_fetch_target(::tensorflow::tpu::CompilationCacheFetchTarget value);
  private:
  ::tensorflow::tpu::CompilationCacheFetchTarget _internal_fetch_target() const;
  void _internal_set_fetch_target(::tensorflow::tpu::CompilationCacheFetchTarget value);
  public:

  // string key = 1;
  bool has_key() const;
  private:
  bool _internal_has_key() const;
  public:
  void clear_key();
  const std::string& key() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_key(ArgT0&& arg0, ArgT... args);
  std::string* mutable_key();
  PROTOBUF_NODISCARD std::string* release_key();
  void set_allocated_key(std::string* key);
  private:
  const std::string& _internal_key() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_key(const std::string& value);
  std::string* _internal_mutable_key();
  public:

  // .tensorflow.tpu.TpuCompilationUidAndIndex uid_and_index = 2;
  bool has_uid_and_index() const;
  private:
  bool _internal_has_uid_and_index() const;
  public:
  void clear_uid_and_index();
  const ::tensorflow::tpu::TpuCompilationUidAndIndex& uid_and_index() const;
  PROTOBUF_NODISCARD ::tensorflow::tpu::TpuCompilationUidAndIndex* release_uid_and_index();
  ::tensorflow::tpu::TpuCompilationUidAndIndex* mutable_uid_and_index();
  void set_allocated_uid_and_index(::tensorflow::tpu::TpuCompilationUidAndIndex* uid_and_index);
  private:
  const ::tensorflow::tpu::TpuCompilationUidAndIndex& _internal_uid_and_index() const;
  ::tensorflow::tpu::TpuCompilationUidAndIndex* _internal_mutable_uid_and_index();
  public:
  void unsafe_arena_set_allocated_uid_and_index(
      ::tensorflow::tpu::TpuCompilationUidAndIndex* uid_and_index);
  ::tensorflow::tpu::TpuCompilationUidAndIndex* unsafe_arena_release_uid_and_index();

  void clear_key_oneof();
  KeyOneofCase key_oneof_case() const;
  // @@protoc_insertion_point(class_scope:tensorflow.tpu.GetTpuProgramRequest)
 private:
  class _Internal;
  void set_has_key();
  void set_has_uid_and_index();

  inline bool has_key_oneof() const;
  inline void clear_has_key_oneof();

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    int fetch_target_;
    union KeyOneofUnion {
      constexpr KeyOneofUnion() : _constinit_{} {}
        ::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized _constinit_;
      ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr key_;
      ::tensorflow::tpu::TpuCompilationUidAndIndex* uid_and_index_;
    } key_oneof_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
    uint32_t _oneof_case_[1];

  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2fcore_2ftpu_2fkernels_2ftpu_5fcompilation_5fcache_5fcommon_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// TpuCompilationUidAndIndex

// int64 uid = 1;
inline void TpuCompilationUidAndIndex::clear_uid() {
  _impl_.uid_ = int64_t{0};
}
inline int64_t TpuCompilationUidAndIndex::_internal_uid() const {
  return _impl_.uid_;
}
inline int64_t TpuCompilationUidAndIndex::uid() const {
  // @@protoc_insertion_point(field_get:tensorflow.tpu.TpuCompilationUidAndIndex.uid)
  return _internal_uid();
}
inline void TpuCompilationUidAndIndex::_internal_set_uid(int64_t value) {
  
  _impl_.uid_ = value;
}
inline void TpuCompilationUidAndIndex::set_uid(int64_t value) {
  _internal_set_uid(value);
  // @@protoc_insertion_point(field_set:tensorflow.tpu.TpuCompilationUidAndIndex.uid)
}

// int32 proto_index = 2;
inline void TpuCompilationUidAndIndex::clear_proto_index() {
  _impl_.proto_index_ = 0;
}
inline int32_t TpuCompilationUidAndIndex::_internal_proto_index() const {
  return _impl_.proto_index_;
}
inline int32_t TpuCompilationUidAndIndex::proto_index() const {
  // @@protoc_insertion_point(field_get:tensorflow.tpu.TpuCompilationUidAndIndex.proto_index)
  return _internal_proto_index();
}
inline void TpuCompilationUidAndIndex::_internal_set_proto_index(int32_t value) {
  
  _impl_.proto_index_ = value;
}
inline void TpuCompilationUidAndIndex::set_proto_index(int32_t value) {
  _internal_set_proto_index(value);
  // @@protoc_insertion_point(field_set:tensorflow.tpu.TpuCompilationUidAndIndex.proto_index)
}

// -------------------------------------------------------------------

// GetTpuProgramRequest

// string key = 1;
inline bool GetTpuProgramRequest::_internal_has_key() const {
  return key_oneof_case() == kKey;
}
inline bool GetTpuProgramRequest::has_key() const {
  return _internal_has_key();
}
inline void GetTpuProgramRequest::set_has_key() {
  _impl_._oneof_case_[0] = kKey;
}
inline void GetTpuProgramRequest::clear_key() {
  if (_internal_has_key()) {
    _impl_.key_oneof_.key_.Destroy();
    clear_has_key_oneof();
  }
}
inline const std::string& GetTpuProgramRequest::key() const {
  // @@protoc_insertion_point(field_get:tensorflow.tpu.GetTpuProgramRequest.key)
  return _internal_key();
}
template <typename ArgT0, typename... ArgT>
inline void GetTpuProgramRequest::set_key(ArgT0&& arg0, ArgT... args) {
  if (!_internal_has_key()) {
    clear_key_oneof();
    set_has_key();
    _impl_.key_oneof_.key_.InitDefault();
  }
  _impl_.key_oneof_.key_.Set( static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:tensorflow.tpu.GetTpuProgramRequest.key)
}
inline std::string* GetTpuProgramRequest::mutable_key() {
  std::string* _s = _internal_mutable_key();
  // @@protoc_insertion_point(field_mutable:tensorflow.tpu.GetTpuProgramRequest.key)
  return _s;
}
inline const std::string& GetTpuProgramRequest::_internal_key() const {
  if (_internal_has_key()) {
    return _impl_.key_oneof_.key_.Get();
  }
  return ::PROTOBUF_NAMESPACE_ID::internal::GetEmptyStringAlreadyInited();
}
inline void GetTpuProgramRequest::_internal_set_key(const std::string& value) {
  if (!_internal_has_key()) {
    clear_key_oneof();
    set_has_key();
    _impl_.key_oneof_.key_.InitDefault();
  }
  _impl_.key_oneof_.key_.Set(value, GetArenaForAllocation());
}
inline std::string* GetTpuProgramRequest::_internal_mutable_key() {
  if (!_internal_has_key()) {
    clear_key_oneof();
    set_has_key();
    _impl_.key_oneof_.key_.InitDefault();
  }
  return _impl_.key_oneof_.key_.Mutable(      GetArenaForAllocation());
}
inline std::string* GetTpuProgramRequest::release_key() {
  // @@protoc_insertion_point(field_release:tensorflow.tpu.GetTpuProgramRequest.key)
  if (_internal_has_key()) {
    clear_has_key_oneof();
    return _impl_.key_oneof_.key_.Release();
  } else {
    return nullptr;
  }
}
inline void GetTpuProgramRequest::set_allocated_key(std::string* key) {
  if (has_key_oneof()) {
    clear_key_oneof();
  }
  if (key != nullptr) {
    set_has_key();
    _impl_.key_oneof_.key_.InitAllocated(key, GetArenaForAllocation());
  }
  // @@protoc_insertion_point(field_set_allocated:tensorflow.tpu.GetTpuProgramRequest.key)
}

// .tensorflow.tpu.TpuCompilationUidAndIndex uid_and_index = 2;
inline bool GetTpuProgramRequest::_internal_has_uid_and_index() const {
  return key_oneof_case() == kUidAndIndex;
}
inline bool GetTpuProgramRequest::has_uid_and_index() const {
  return _internal_has_uid_and_index();
}
inline void GetTpuProgramRequest::set_has_uid_and_index() {
  _impl_._oneof_case_[0] = kUidAndIndex;
}
inline void GetTpuProgramRequest::clear_uid_and_index() {
  if (_internal_has_uid_and_index()) {
    if (GetArenaForAllocation() == nullptr) {
      delete _impl_.key_oneof_.uid_and_index_;
    }
    clear_has_key_oneof();
  }
}
inline ::tensorflow::tpu::TpuCompilationUidAndIndex* GetTpuProgramRequest::release_uid_and_index() {
  // @@protoc_insertion_point(field_release:tensorflow.tpu.GetTpuProgramRequest.uid_and_index)
  if (_internal_has_uid_and_index()) {
    clear_has_key_oneof();
    ::tensorflow::tpu::TpuCompilationUidAndIndex* temp = _impl_.key_oneof_.uid_and_index_;
    if (GetArenaForAllocation() != nullptr) {
      temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
    }
    _impl_.key_oneof_.uid_and_index_ = nullptr;
    return temp;
  } else {
    return nullptr;
  }
}
inline const ::tensorflow::tpu::TpuCompilationUidAndIndex& GetTpuProgramRequest::_internal_uid_and_index() const {
  return _internal_has_uid_and_index()
      ? *_impl_.key_oneof_.uid_and_index_
      : reinterpret_cast< ::tensorflow::tpu::TpuCompilationUidAndIndex&>(::tensorflow::tpu::_TpuCompilationUidAndIndex_default_instance_);
}
inline const ::tensorflow::tpu::TpuCompilationUidAndIndex& GetTpuProgramRequest::uid_and_index() const {
  // @@protoc_insertion_point(field_get:tensorflow.tpu.GetTpuProgramRequest.uid_and_index)
  return _internal_uid_and_index();
}
inline ::tensorflow::tpu::TpuCompilationUidAndIndex* GetTpuProgramRequest::unsafe_arena_release_uid_and_index() {
  // @@protoc_insertion_point(field_unsafe_arena_release:tensorflow.tpu.GetTpuProgramRequest.uid_and_index)
  if (_internal_has_uid_and_index()) {
    clear_has_key_oneof();
    ::tensorflow::tpu::TpuCompilationUidAndIndex* temp = _impl_.key_oneof_.uid_and_index_;
    _impl_.key_oneof_.uid_and_index_ = nullptr;
    return temp;
  } else {
    return nullptr;
  }
}
inline void GetTpuProgramRequest::unsafe_arena_set_allocated_uid_and_index(::tensorflow::tpu::TpuCompilationUidAndIndex* uid_and_index) {
  clear_key_oneof();
  if (uid_and_index) {
    set_has_uid_and_index();
    _impl_.key_oneof_.uid_and_index_ = uid_and_index;
  }
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:tensorflow.tpu.GetTpuProgramRequest.uid_and_index)
}
inline ::tensorflow::tpu::TpuCompilationUidAndIndex* GetTpuProgramRequest::_internal_mutable_uid_and_index() {
  if (!_internal_has_uid_and_index()) {
    clear_key_oneof();
    set_has_uid_and_index();
    _impl_.key_oneof_.uid_and_index_ = CreateMaybeMessage< ::tensorflow::tpu::TpuCompilationUidAndIndex >(GetArenaForAllocation());
  }
  return _impl_.key_oneof_.uid_and_index_;
}
inline ::tensorflow::tpu::TpuCompilationUidAndIndex* GetTpuProgramRequest::mutable_uid_and_index() {
  ::tensorflow::tpu::TpuCompilationUidAndIndex* _msg = _internal_mutable_uid_and_index();
  // @@protoc_insertion_point(field_mutable:tensorflow.tpu.GetTpuProgramRequest.uid_and_index)
  return _msg;
}

// .tensorflow.tpu.CompilationCacheFetchTarget fetch_target = 3;
inline void GetTpuProgramRequest::clear_fetch_target() {
  _impl_.fetch_target_ = 0;
}
inline ::tensorflow::tpu::CompilationCacheFetchTarget GetTpuProgramRequest::_internal_fetch_target() const {
  return static_cast< ::tensorflow::tpu::CompilationCacheFetchTarget >(_impl_.fetch_target_);
}
inline ::tensorflow::tpu::CompilationCacheFetchTarget GetTpuProgramRequest::fetch_target() const {
  // @@protoc_insertion_point(field_get:tensorflow.tpu.GetTpuProgramRequest.fetch_target)
  return _internal_fetch_target();
}
inline void GetTpuProgramRequest::_internal_set_fetch_target(::tensorflow::tpu::CompilationCacheFetchTarget value) {
  
  _impl_.fetch_target_ = value;
}
inline void GetTpuProgramRequest::set_fetch_target(::tensorflow::tpu::CompilationCacheFetchTarget value) {
  _internal_set_fetch_target(value);
  // @@protoc_insertion_point(field_set:tensorflow.tpu.GetTpuProgramRequest.fetch_target)
}

inline bool GetTpuProgramRequest::has_key_oneof() const {
  return key_oneof_case() != KEY_ONEOF_NOT_SET;
}
inline void GetTpuProgramRequest::clear_has_key_oneof() {
  _impl_._oneof_case_[0] = KEY_ONEOF_NOT_SET;
}
inline GetTpuProgramRequest::KeyOneofCase GetTpuProgramRequest::key_oneof_case() const {
  return GetTpuProgramRequest::KeyOneofCase(_impl_._oneof_case_[0]);
}
#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace tpu
}  // namespace tensorflow

PROTOBUF_NAMESPACE_OPEN

template <> struct is_proto_enum< ::tensorflow::tpu::CompilationCacheFetchTarget> : ::std::true_type {};
template <>
inline const EnumDescriptor* GetEnumDescriptor< ::tensorflow::tpu::CompilationCacheFetchTarget>() {
  return ::tensorflow::tpu::CompilationCacheFetchTarget_descriptor();
}

PROTOBUF_NAMESPACE_CLOSE

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcore_2ftpu_2fkernels_2ftpu_5fcompilation_5fcache_5fcommon_2eproto
