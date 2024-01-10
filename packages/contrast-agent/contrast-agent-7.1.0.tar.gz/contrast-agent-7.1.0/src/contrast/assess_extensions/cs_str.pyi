# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.


def in_contrast_or_propagation_scope() -> bool:
    ...


def has_funchook() -> bool:
    ...


def get_current_scope() -> tuple:
    ...


def set_exact_scope(scope: tuple[int, int, int], /) -> None:
    ...


def get_tp_version_tag(type: type, /) -> int:
    ...


def set_attr_on_type(owner: type, name: str, value, /) -> None:
    ...
