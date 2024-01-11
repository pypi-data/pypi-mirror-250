"""Material icons' settings icon class implementation.
"""

from typing import Optional
from typing import Union

from apysc._color.color import Color
from apysc._display.child_mixin import ChildMixIn
from apysc._material_design.icon.material_icon_base import MaterialIconBase
from apysc._type.int import Int
from apysc._type.number import Number
from apysc._validation import arg_validation_decos


class MaterialSettingsIcon(MaterialIconBase):
    """
    Material icons' settings icon class implementation.

    References
    ----------
    - Material icons
        - https://fonts.google.com/icons?selected=Material+Icons:search:
    - APACHE LICENSE, VERSION 2.0
        - https://www.apache.org/licenses/LICENSE-2.0.html
    """

    # fill_color
    @arg_validation_decos.is_color(arg_position_index=1, optional=False)
    # fill_alpha
    @arg_validation_decos.is_num(arg_position_index=2, optional=False)
    # x
    @arg_validation_decos.is_num(arg_position_index=3, optional=False)
    # y
    @arg_validation_decos.is_num(arg_position_index=4, optional=False)
    # width
    @arg_validation_decos.num_is_gte_zero(arg_position_index=5, optional=False)
    # height
    @arg_validation_decos.num_is_gte_zero(arg_position_index=6, optional=False)
    # parent
    @arg_validation_decos.is_display_object_container(
        arg_position_index=7, optional=True
    )
    # variable_name_suffix
    @arg_validation_decos.is_builtin_string(arg_position_index=8, optional=False)
    def __init__(
        self,
        *,
        fill_color: Color,
        fill_alpha: Union[float, Number] = 1.0,
        x: Union[float, Number] = 0,
        y: Union[float, Number] = 0,
        width: Union[int, Int] = 24,
        height: Union[int, Int] = 24,
        parent: Optional[ChildMixIn] = None,
        variable_name_suffix: str = "",
    ) -> None:
        """
        Material icons' settings icon class implementation.

        Parameters
        ----------
        fill_color : Color
            An icon fill-color.
        fill_alpha : Union[float, Number], optional
            An icon fill-alpha (opacity).
        x : Union[float, Number], optional
            An icon x-coordinate.
        y : Union[float, Number], optional
            An icon y-coordinate.
        width : Union[int, Int], optional
            An icon width.
        height : Union[int, Int], optional
            An icon height.
        parent : ChildMixIn or None, default None
            A parent instance to add this instance.
            If the specified value is None, this interface uses
            a stage instance.
        variable_name_suffix : str, optional
            A JavaScript variable name suffix string.
            This setting is sometimes useful for JavaScript debugging.

        References
        ----------
        - Material icons
            - https://fonts.google.com/icons?selected=Material+Icons:search:
        - APACHE LICENSE, VERSION 2.0
            - https://www.apache.org/licenses/LICENSE-2.0.html
        """
        from apysc._expression import expression_variables_util
        from apysc._expression import var_names

        variable_name: str = expression_variables_util.get_next_variable_name(
            type_name=var_names.MATERIAL_SETTINGS_ICON,
        )
        super(MaterialSettingsIcon, self).__init__(
            svg_path_value="M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.74,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z",  # noqa
            fill_color=fill_color,
            fill_alpha=fill_alpha,
            x=x,
            y=y,
            width=width,
            height=height,
            parent=parent,
            variable_name=variable_name,
            variable_name_suffix=variable_name_suffix,
        )
