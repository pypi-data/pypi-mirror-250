#  Copyright© 2023 Raúl Wolters(1)
#
#  This file is part of Inflatox.
#
#  Inflatox is free software: you can redistribute it and/or modify it under
#  the terms of the European Union Public License version 1.2 or later, as
#  published by the European Commission.
#
#  Inflatox is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE. See the European Union Public License for more details.
#
#  You should have received a copy of the EUPL in an/all official language(s) of
#  the European Union along with Inflatox.  If not, see 
#  <https://ec.europa.eu/info/european-union-public-licence_en/>.
#
#  (1) Resident of the Kingdom of the Netherlands; agreement between licensor and
#  licensee subject to Dutch law as per article 15 of the EUPL.

#External imports
from inflatox.compiler import CompilationArtifact
import numpy as np

#Internal imports
from .compiler import CompilationArtifact
from .libinflx_rs import *

#Limit exports to these items
__all__ = ['InflationCondition', 'AnguelovaLazaroiuCondition']

class InflationCondition():
  """Base class for all inflation conditions. Provides native methods to evaluate
  the potential and projected Hesse matrix. This base-class may be extended either
  by using these native methods, or by including your own native code that hooks
  into the Rust API or C ABI.
  """

  def __init__(self, compiled_artifact: CompilationArtifact):
    self.artifact = compiled_artifact
    self.dylib = open_inflx_dylib(compiled_artifact.shared_object_path)
    
  def calc_V(self, x: np.ndarray, args: np.ndarray) -> float:
    """calculates the scalar potential at field-space coordinates `x` with
    model-specific parameters `args`.

    ### Args
    - `x` (`np.ndarray`): field-space coordinates at which to calculate
    - `args` (`np.ndarray`): values of the model-dependent parameters. See
    `CompilationArtifact.print_sym_lookup_table()` for an overview of which
    sympy symbols were mapped to which args index.

    ### Returns
      `float`: Value of scalar potential with parameters `args` at coordinates `x`.
    """
    return self.dylib.potential(x, args)
  
  def calc_V_array(self,
    args: list[float] | np.ndarray,
    start: list[float] | np.ndarray,
    stop: list[float] | np.ndarray,
    N: list[int] | None = None
  ) -> np.ndarray:
    """constructs an array of field space coordinates and fills it with the
    value of the scalar potential at those field space coordinates.
    The start and stop values of each axis in field-space can be specified with
    the `start` and `stop` arguments. The number of samples along each axis can
    be set with the `N` argument. It defaults to `8000` per axis.

    ### Args
    - `args` (`list[float] | np.ndarray`): values of the model-dependent
    parameters. See `CompilationArtifact.print_sym_lookup_table()` for an
    overview of which sympy symbols were mapped to which args index.
    - `start` (`list[float] | np.ndarray`): list of minimum values for
    each axis of the to-be-constructed array in field space.
    - `stop` (`list[float] | np.ndarray`): list of maximum values for each
    axis of the to-be-constructed array in field space.
    - `N` (`list[int] | None`, optional): _description_. list of the number of
    samples along each axis in field space. If set to `None`, 8000 samples will
    be used along each axis.

    ### Returns
    `np.ndarray`: value of scalar potential at specified field-space
    coordinates
    """
    n_fields = self.artifact.n_fields
    start_stop = np.array([[start, stop] for (start, stop) in zip(start, stop)])
    N = N if N is not None else (8000 for _ in range(n_fields))
    x = np.zeros(N)
    self.dylib.potential_array(x, args, start_stop)
    return x
  
  def calc_H(self, x: np.ndarray, args: np.ndarray) -> np.ndarray:
    """calculates the projected covariant Hesse matrix at field-space
    coordinates `x` with model-specific parameters `args`.

    ### Args
    - `x` (`np.ndarray`): field-space coordinates at which to calculate
    - `args` (`np.ndarray`): values of the model-dependent parameters. See
    `CompilationArtifact.print_sym_lookup_table()` for an overview of which
    sympy symbols were mapped to which args index.

    ### Returns
    `np.ndarray`: Components of the projected covariant hesse matrix with
      parameters `args` at coordinates `x`.
    """
    return self.dylib.hesse(x, args)
  
  def calc_H_array(self,
    args: list[float] | np.ndarray,
    start: list[float] | np.ndarray,
    stop: list[float] | np.ndarray,
    N: list[int] | None = None
  ) -> np.ndarray:
    """constructs an array of field space coordinates and fills it with the
    value of the projected Hesse matrix at those field space coordinates.
    The start and stop values of each axis in field-space can be specified with
    the `start` and `stop` arguments. The number of samples along each axis can
    be set with the `N` argument. It defaults to `8000` per axis.

    ### Args
    - `args` (`list[float] | np.ndarray`): values of the model-dependent
    parameters. See `CompilationArtifact.print_sym_lookup_table()` for an
    overview of which sympy symbols were mapped to which args index.
    - `start` (`list[float] | np.ndarray`): list of minimum values for
    each axis of the to-be-constructed array in field space.
    - `stop` (`list[float] | np.ndarray`): list of maximum values for each
    axis of the to-be-constructed array in field space.
    - `N` (`list[int] | None`, optional): _description_. list of the number of
    samples along each axis in field space. If set to `None`, 8000 samples will
    be used along each axis.

    ### Returns
    `np.ndarray`: (d+2)-dimensional array for a d-dimensional field-space. The
      first two axes of this array represent the axes of the Hesse matrix itself.
      The other axes correspond to the field-space components. 
    """
    n_fields = self.artifact.n_fields
    start_stop = np.array([[start, stop] for (start, stop) in zip(start, stop)])
    N = N if N is not None else (8000 for _ in range(n_fields))
    return self.dylib.hesse_array(N, args, start_stop)

class AnguelovaLazaroiuCondition(InflationCondition):
  """This class extends the generic `InflationCondition` with the potential
  consistency condition from Anguelova and Lazaroiu 2022 paper
  (`arXiv:2210.00031v2`) for rapid-turn, slow-roll (RTSL) inflationary models.

  ### Usage
  To construct an instance of this class, a `CompilationArtifact` is required.
  Such an artifact can be obtained by running an instance of `inflatox.Compiler`
  with a specific model (fieldspace metric + scalar potential). For more info on
  how to use the `Compiler`, see its documentation.
  
  The artifact contains all the necessary information to evaluate the consistency
  condition and can be used to construct an instance of this class.
  
  To run evaluate the consistency condition for various model parameters and
  regions of field-space, use the `.evaluate()` method on an instance of this class
  with the appropriate methods. For more info, see the `.evaluate()` method.
  """
  
  def __init__(self, compiled_artifact: CompilationArtifact):
    super().__init__(compiled_artifact)
    
  def evaluate(self,
    args: np.ndarray,
    x0_start: float,
    x0_stop: float,
    x1_start: float,
    x1_stop: float,
    N_x0: int = 10_000,
    N_x1: int = 10_000,
    order: ['exact', 'leading', '0th', '2nd'] = '2nd',
    progress: bool = True
  ) -> np.ndarray:
    """Evaluates the potential consistency condition from Anguelova and Lazaroiu
    2022 paper (`arXiv:2210.00031v2`) for rapid-turn, slow-roll (RTSL)
    inflationary models.
    
    In their paper, the authors claim that RTSL models must satisfy a consistency
    condition:
      3V (V_vv)^2 = (V_vw)^2 V_ww
    Where V_ab are the components of the covariant Hesse matrix projected along
    the vectors a and b. v is the basis vector parallel to the gradient of the scalar
    potential V and w is the second basis vector (orthonormal to v).
    
    This function returns the difference between the left-hand side (lhs) divided
    by the right-hand side (rhs) of the consistency condition from
    Anguelova & Lazaroiu, minus one:
      3(V_vv / V_vw)^2 = V_ww / V
    Hence the output will be:
      out = lhs / rhs - 1
    The field-space region to be investigated is specified with the arguments of
    this function.

    ### Args
    General: See `CompilationArtifact.print_sym_lookup_table()` for an overview
    of which sympy symbols were mapped to which arguments (args) and fields (x).
    - `args` (`np.ndarray`): values of the model-dependent parameters. 
    - `x0_start` (`float`): minimum value of first field `x[0]`.
    - `x0_stop` (`float`): maximum value of first field `x[0]`.
    - `x1_start` (`float`): minimum value of second field `x[1]`.
    - `y_stop` (`float`): maximum value of second field `x[1]`.
    - `N_x` (`int`, optional): number of steps along `x[0]` axis. Defaults to 10_000.
    - `x1_stop` (`int`, optional): number of steps along `x[1]` axis. Defaults to 10_000.
    - `order (['exact', 'leading', '0th', '2nd'], optional)`: set approximation order
      for AL consistency condition. See [reference] for details. Defaults to 2nd.
    - `progress` (`bool`, optional): whether to render a progressbar or not. Showing the
      progressbar may slightly degrade performance. Defaults to True.

    ### Returns
    `np.ndarray`: Quotient of left-hand side and right-hand side of
    Anguelova & Lazaroiu consistency condition (approximated to the specified
    order), minus one.
      
    ### Example
    Run and plot the consistency condition
    ```python
    from inflatox.consistency_conditions import AnguelovaLazaroiuCondition
    from matplotlib import pyplot as plt
    anguelova = AnguelovaLazaroiuCondition(comp_artifact)

    #calculate condition
    args = np.ndarray([3.4e-10, 5e-16, 2.5e-3, 1.0])
    x = np.ndarray([2.0, 2.0])
    extent = (-1e-3, 1e-3, -1e-3, 1e-3)
    array = anguelova.evaluate(args, *extent)
    
    #plot result
    plt.imshow(array, extent=extent)
    plt.colorbar()
    plt.show()
    ```
    """
    #set up args for anguelova's condition
    x = np.zeros((N_x0, N_x1))
    
    start_stop = np.array([
      [x0_start, x0_stop],
      [x1_start, x1_stop]
    ])
    
    order_int = 10
    if order == 'exact': order_int = -2
    elif order == 'leading': order_int = -1
    elif order == '0th': order_int = 0
    elif order == '2nd': order_int = 2
    else: raise Exception(f'order parameter was set to \"{order}\". Expected one of the following options: [\'exact\', \'leading\', \'0th\', \'2nd\']')
    
    #evaluate and return
    anguelova_py(self.dylib, args, x, start_stop, order_int, progress)
    return x

  def calc_delta(self,
    args: np.ndarray,
    x0_start: float,
    x0_stop: float,
    x1_start: float,
    x1_stop: float,
    N_x0: int = 10_000,
    N_x1: int = 10_000,
    progress = True
  ) -> np.ndarray:
    """Evaluates the characteristic angle δ for the field-space region specified
    by the start/stop arguments given some model parameters. See [publication] for
    the definition and interpretation of δ.
    
    ### Precise mathematical formulation
    δ is calculated by taking the arctangent of the quotient of Vvw and Vvv. Vvw
    is the inner product of the covariant Hesse matrix with vectors of the gradient
    basis {v,w} where v is aligned with the gradient of the potential and w is
    perpendicular to v. Similarly, Vvv is the covariant Hesse matrix projected
    onto v twice. δ is clamped between -π/2 and +π/2.

    ### Args
    - `args` (`np.ndarray`): values of the model-dependent parameters. 
    - `x0_start` (`float`): minimum value of first field `x[0]`.
    - `x0_stop` (`float`): maximum value of first field `x[0]`.
    - `x1_start` (`float`): minimum value of second field `x[1]`.
    - `y_stop` (`float`): maximum value of second field `x[1]`.
    - `N_x` (`int`, optional): number of steps along `x[0]` axis. Defaults to 10_000.
    - `x1_stop` (`int`, optional): number of steps along `x[1]` axis. Defaults to 10_000.
    - `progress` (`bool`, optional): whether to render a progressbar or not. Showing the
      progressbar may slightly degrade performance. Defaults to True.

    ### Returns
    `np.ndarray`: array with calculated δ's
    """
    #set up args for anguelova's condition
    x = np.zeros((N_x0, N_x1))
    
    start_stop = np.array([
      [x0_start, x0_stop],
      [x1_start, x1_stop]
    ])
    
    #evaluate and return
    delta_py(self.dylib, args, x, start_stop, progress)
    return x
  
  def calc_omega(self,
    args: np.ndarray,
    x0_start: float,
    x0_stop: float,
    x1_start: float,
    x1_stop: float,
    N_x0: int = 10_000,
    N_x1: int = 10_000,
    progress = True
  ) -> np.ndarray:
    """Evaluates the turn rate ω for the field-space region specified by the
    start/stop arguments given the model parameters, assuming that all slow-roll
    parameters are small.
    
    ### Precise mathematical formulation
    When the slow-roll parameters are zero, ω can be written as:
    
      Vtt / V = ω²/3
      
    In this range, we can thus calculate ω from the potential and field-space
    metric alone. See [publication] for more details and examples. Vtt is written
    in terms of Vvv, Vvw and Vww using the angle δ:
  
    Vtt = cos²δ Vww + sin²δ -2sinδ cosδ Vvw

    ### Args
    - `args` (`np.ndarray`): values of the model-dependent parameters. 
    - `x0_start` (`float`): minimum value of first field `x[0]`.
    - `x0_stop` (`float`): maximum value of first field `x[0]`.
    - `x1_start` (`float`): minimum value of second field `x[1]`.
    - `y_stop` (`float`): maximum value of second field `x[1]`.
    - `N_x` (`int`, optional): number of steps along `x[0]` axis. Defaults to 10_000.
    - `x1_stop` (`int`, optional): number of steps along `x[1]` axis. Defaults to 10_000.
    - `progress` (`bool`, optional): whether to render a progressbar or not. Showing the
      progressbar may slightly degrade performance. Defaults to True.

    ### Returns
    `np.ndarray`: array with calculated ω's
    """
    #set up args for anguelova's condition
    x = np.zeros((N_x0, N_x1))
    
    start_stop = np.array([
      [x0_start, x0_stop],
      [x1_start, x1_stop]
    ])
    
    #evaluate and return
    omega_py(self.dylib, args, x, start_stop, progress)
    return x
  
  def calc_epsilon(self,
    args: np.ndarray,
    x0_start: float,
    x0_stop: float,
    x1_start: float,
    x1_stop: float,
    N_x0: int = 10_000,
    N_x1: int = 10_000,
    progress = True
  ) -> np.ndarray:
    """Evaluates the turn rate ω for the field-space region specified by the
    start/stop arguments given the model parameters, assuming that all slow-roll
    parameters are small.
    
    ### Precise mathematical formulation
    When the slow-roll parameters are zero, ω can be written as:
    
      Vtt / V = ω²/3
      
    In this range, we can thus calculate ω from the potential and field-space
    metric alone. See [publication] for more details and examples. Vtt is written
    in terms of Vvv, Vvw and Vww using the angle δ:
  
    Vtt = cos²δ Vww + sin²δ -2sinδ cosδ Vvw

    ### Args
    - `args` (`np.ndarray`): values of the model-dependent parameters. 
    - `x0_start` (`float`): minimum value of first field `x[0]`.
    - `x0_stop` (`float`): maximum value of first field `x[0]`.
    - `x1_start` (`float`): minimum value of second field `x[1]`.
    - `y_stop` (`float`): maximum value of second field `x[1]`.
    - `N_x` (`int`, optional): number of steps along `x[0]` axis. Defaults to 10_000.
    - `x1_stop` (`int`, optional): number of steps along `x[1]` axis. Defaults to 10_000.
    - `progress` (`bool`, optional): whether to render a progressbar or not. Showing the
      progressbar may slightly degrade performance. Defaults to True.

    ### Returns
    `np.ndarray`: array with calculated ω's
    """
    #set up args for anguelova's condition
    x = np.zeros((N_x0, N_x1))
    
    start_stop = np.array([
      [x0_start, x0_stop],
      [x1_start, x1_stop]
    ])
    
    #evaluate and return
    epsilon_py(self.dylib, args, x, start_stop, progress)
    return x
  
  def flag_quantum_dif(self,
      args: np.ndarray,
      x0_start: float,
      x0_stop: float,
      x1_start: float,
      x1_stop: float,
      N_x0: int = 10_000,
      N_x1: int = 10_000,
      progress = True,
      accuracy = 1e-3
    ) -> np.ndarray:
    """returns boolean array where `True` values indicate that both components
    of the gradient of the scalar potential are smaller than the specified
    `accuracy` parameter. This is useful to identify points in the potential where
    quantum diffusion may have a large impact (saddle points in the potential).
    This calculation explicitly *does not* take into account the full inner product
    using the metric to avoid measuring where the metric goes to zero or becomes
    signular.

    Args:
    - `args` (`np.ndarray`): values of the model-dependent parameters. 
    - `x0_start` (`float`): minimum value of first field `x[0]`.
    - `x0_stop` (`float`): maximum value of first field `x[0]`.
    - `x1_start` (`float`): minimum value of second field `x[1]`.
    - `y_stop` (`float`): maximum value of second field `x[1]`.
    - `N_x` (`int`, optional): number of steps along `x[0]` axis. Defaults to 10_000.
    - `x1_stop` (`int`, optional): number of steps along `x[1]` axis. Defaults to 10_000.
    - `progress` (`bool`, optional): whether to render a progressbar or not. Showing the
      progressbar may slightly degrade performance. Defaults to True.
    - `accuracy` (`float`, optional): 

    Returns:
    `np.ndarray`: boolean array. `True` where the absolute value of both components
      of the gradient are smaller than `accuracy`, `False` otherwise.
    """
    
    #set up args for anguelova's condition
    x = np.zeros((N_x0, N_x1), dtype=bool)
    
    start_stop = np.array([
      [x0_start, x0_stop],
      [x1_start, x1_stop]
    ])
    
    #evaluate and return
    flag_quantum_dif_py(self.dylib, args, x, start_stop, progress, accuracy)
    return x
