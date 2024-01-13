subroutine gammaln(x, val, N) bind(c, name='gammaln')
  use iso_c_binding
  use special_functions

  implicit none

  integer, parameter :: dp = selected_real_kind(15, 307)

  integer(c_int), intent(in), value :: N
  real(c_double), intent(in) :: x(N)
  real(c_double), intent(out) :: val(N)

  integer :: i
  real(dp) :: gl
  real(dp) :: x_in

  do i = 1, N
     x_in = real(x(i), dp)
     call lgama(2, x_in, gl)
     val(i) = real(gl, c_double)
  end do
  return
end subroutine gammaln

subroutine hyp1f1(a, b, zr, zc, chgr, chgc, N, kf) bind(c, name='hyp1f1')
  use iso_c_binding
  use special_functions

  implicit none

  integer, parameter :: dp = selected_real_kind(15, 307)
  integer, parameter :: cd = (dp, dp)

  integer(c_int), intent(in), value :: N
  integer(c_int), intent(in), value :: kf  ! 1 for hyp1f1 else log(hyp1f1)
  real(c_double), intent(in) :: a(N), b(N), zr(N), zc(N)
  real(c_double), intent(out) :: chgr(N), chgc(N)

  complex(cd) :: z(N), chg(N)
  integer :: i

  z = cmplx(real(zr, dp), real(zc, dp))

  do i = 1, N
     call cchg(real(a(i), dp), real(b(i), dp), z(i), chg(i))
  end do

  if (int(kf) == 1) then
     chgr = chg%re
     chgc = chg%im
  else
     chgr = log(chg%re)
     chgc = log(chg%im)
  end if

  return
end subroutine hyp1f1

