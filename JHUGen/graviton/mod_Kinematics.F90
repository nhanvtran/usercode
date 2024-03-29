MODULE ModKinematics
implicit none
save


type :: Histogram
    integer :: NBins
    real(8) :: BinSize
    real(8) :: LowVal
    real(8) :: SetScale
    real(8) :: Value(0:300)
    real(8) :: Value2(0:300)
    integer :: Hits(0:300)
    character :: Info*(50)
end type

integer,public :: it_sav
type(Histogram),allocatable :: Histo(:)

contains


SUBROUTINE WriteOutEvent(Mom,MY_IDUP,ICOLUP)
use ModParameters
implicit none
real(8) :: Mom(1:4,1:6)
real(8) :: Spin, Lifetime
real(8) :: XFV(1:4), Z1FV(1:4), Z2FV(1:4)
real(8) :: MomDummy(1:4,1:6)
real(8) :: Part1Mass,Part2Mass,XMass,Z1Mass,Z2Mass,L11Mass,L12Mass,L21Mass,L22Mass
integer :: a,b,c
integer :: MY_IDUP(1:9),LHE_IDUP(1:9),i,ISTUP(1:9),MOTHUP(1:2,1:9),ICOLUP(1:2,1:9)
integer :: NUP,IDPRUP
real(8) :: XWGTUP,SCALUP,AQEDUP,AQCDUP
real(8) :: ntRnd
character(len=*),parameter :: fmt1 = "(I3,X,I2,X,I2,X,I2,X,I3,X,I3,X,1PE14.7,X,1PE14.7,X,1PE14.7,X,1PE14.7,X,1PE14.7,X,1PE14.7,X,1PE14.7)"

	!!!!!! Randomize lepton channel
	call random_number(ntRnd)
	if( DecayMode.eq.0 ) then
		if ((ntRnd .GE. 0.0) .AND. (ntRnd .LE. 0.25)) then
		MY_IDUP(6:9) =(/ElM_,ElP_,MuM_,MuP_/)
		elseif ((ntRnd .GT. 0.25) .AND. (ntRnd .LE. 0.50)) then
		MY_IDUP(6:9) =(/MuM_,MuP_,ElM_,ElP_/)
		elseif ((ntRnd .GT. 0.50) .AND. (ntRnd .LE. 0.75)) then
		MY_IDUP(6:9) =(/ElM_,ElP_,ElM_,ElP_/)
		elseif ((ntRnd .GT. 0.75) .AND. (ntRnd .LE. 1.0)) then
		MY_IDUP(6:9) =(/MuM_,MuP_,MuM_,MuP_/)
		endif
	endif
	if( DecayMode.eq.1 ) then
		if ((ntRnd .GE. 0.0) .AND. (ntRnd .LE. 0.50)) then
		MY_IDUP(6:7) =(/ElM_,ElP_/)
		elseif ((ntRnd .GT. 0.50) .AND. (ntRnd .LE. 1.0)) then
		MY_IDUP(6:7) =(/MuM_,MuP_/)
		endif
	endif

    do i=1,9
        LHE_IDUP(i) = convertLHE( MY_IDUP(i) )
    enddo


    NUP=9
    IDPRUP=100
    XWGTUP=1.
    SCALUP=1000.
    AQEDUP=alpha_QED
    AQCDUP=0d0

    ISTUP(1) = - 1
    ISTUP(2) =  -1
    ISTUP(3) = 2
    ISTUP(4) = 2
    ISTUP(5) = 2
    ISTUP(6) = 1
    ISTUP(7) = 1
    ISTUP(8) = 1
    ISTUP(9) = 1

    MOTHUP(1,1) = 0
    MOTHUP(2,1) = 0
    MOTHUP(1,2) = 0
    MOTHUP(2,2) = 0
    MOTHUP(1,3) = 1
    MOTHUP(2,3) = 2
    MOTHUP(1,4) = 3
    MOTHUP(2,4) = 3
    MOTHUP(1,5) = 3
    MOTHUP(2,5) = 3
    MOTHUP(1,6) = 4
    MOTHUP(2,6) = 4
    MOTHUP(1,7) = 4
    MOTHUP(2,7) = 4
    MOTHUP(1,8) = 5
    MOTHUP(2,8) = 5
    MOTHUP(1,9) = 5
    MOTHUP(2,9) = 5

	! Added by Nhan
	LHE_IDUP(3) = 39 ! X particle
	Lifetime = 0.0
	Spin = 1.0

	do a=1,6
		MomDummy(1,a) = 100.*Mom(1,a)
		MomDummy(2,a) = 100.*Mom(2,a)
		MomDummy(3,a) = 100.*Mom(3,a)
		MomDummy(4,a) = 100.*Mom(4,a)
	enddo

	do b=1,4
		Z1FV(b) = MomDummy(b,3)+MomDummy(b,4)
		Z2FV(b) = MomDummy(b,5)+MomDummy(b,6)
	enddo

	do c=1,4
		XFV(c) = Z1FV(c) + Z2FV(c)
	enddo

	Part1Mass = SQRT(MomDummy(1,1)*MomDummy(1,1)-MomDummy(2,1)*MomDummy(2,1)-MomDummy(3,1)*MomDummy(3,1)-MomDummy(4,1)*MomDummy(4,1))
	Part2Mass = SQRT(MomDummy(1,2)*MomDummy(1,2)-MomDummy(2,2)*MomDummy(2,2)-MomDummy(3,2)*MomDummy(3,2)-MomDummy(4,2)*MomDummy(4,2))

	XMass = SQRT(XFV(1)*XFV(1)-XFV(2)*XFV(2)-XFV(3)*XFV(3)-XFV(4)*XFV(4))
	Z1Mass = SQRT(Z1FV(1)*Z1FV(1)-Z1FV(2)*Z1FV(2)-Z1FV(3)*Z1FV(3)-Z1FV(4)*Z1FV(4))
	Z2Mass = SQRT(Z2FV(1)*Z2FV(1)-Z2FV(2)*Z2FV(2)-Z2FV(3)*Z2FV(3)-Z2FV(4)*Z2FV(4))

	L11Mass = SQRT(ABS(MomDummy(1,3)*MomDummy(1,3)-MomDummy(2,3)*MomDummy(2,3)-MomDummy(3,3)*MomDummy(3,3)-MomDummy(4,3)*MomDummy(4,3)))
	L12Mass = SQRT(ABS(MomDummy(1,4)*MomDummy(1,4)-MomDummy(2,4)*MomDummy(2,4)-MomDummy(3,4)*MomDummy(3,4)-MomDummy(4,4)*MomDummy(4,4)))
	L21Mass = SQRT(ABS(MomDummy(1,5)*MomDummy(1,5)-MomDummy(2,5)*MomDummy(2,5)-MomDummy(3,5)*MomDummy(3,5)-MomDummy(4,5)*MomDummy(4,5)))
	L22Mass = SQRT(ABS(MomDummy(1,6)*MomDummy(1,6)-MomDummy(2,6)*MomDummy(2,6)-MomDummy(3,6)*MomDummy(3,6)-MomDummy(4,6)*MomDummy(4,6)))


    write(14,"(A)") "<event>"
    write(14,"(I1,X,I3,X,1PE13.7,X,1PE13.7,X,1PE13.7,X,1PE13.7)") NUP,IDPRUP,XWGTUP,SCALUP,AQEDUP,AQCDUP

! parton_a
    i=1
    write(14,fmt1) LHE_IDUP(i),ISTUP(i), MOTHUP(1,i),MOTHUP(2,i), ICOLUP(1,i),ICOLUP(2,i),MomDummy(2:4,1),MomDummy(1,1),Part1Mass,Lifetime,Spin

! parton_b
    i=2
    write(14,fmt1) LHE_IDUP(i),ISTUP(i), MOTHUP(1,i),MOTHUP(2,i), ICOLUP(1,i),ICOLUP(2,i),MomDummy(2:4,2),MomDummy(1,2),Part2Mass,Lifetime,Spin

! X
    i=3
    write(14,fmt1) LHE_IDUP(i),ISTUP(i), MOTHUP(1,i),MOTHUP(2,i), ICOLUP(1,i),ICOLUP(2,i),XFV(2:4),XFV(1),XMass,Lifetime,Spin

! Z1
    i=4
    write(14,fmt1) LHE_IDUP(i),ISTUP(i), MOTHUP(1,i),MOTHUP(2,i), ICOLUP(1,i),ICOLUP(2,i),Z1FV(2:4),Z1FV(1),Z1Mass,Lifetime,Spin

! Z2
    i=5
    write(14,fmt1) LHE_IDUP(i),ISTUP(i), MOTHUP(1,i),MOTHUP(2,i), ICOLUP(1,i),ICOLUP(2,i),Z2FV(2:4),Z2FV(1),Z2Mass,Lifetime,Spin


! lepton 1+
    i=7
    write(14,fmt1) LHE_IDUP(i),ISTUP(i), MOTHUP(1,i),MOTHUP(2,i), ICOLUP(1,i),ICOLUP(2,i),MomDummy(2:4,3),MomDummy(1,3),L12Mass,Lifetime,Spin

! lepton 1-
    i=6
    write(14,fmt1) LHE_IDUP(i),ISTUP(i), MOTHUP(1,i),MOTHUP(2,i), ICOLUP(1,i),ICOLUP(2,i),MomDummy(2:4,4),MomDummy(1,4),L11Mass,Lifetime,Spin

! lepton 2+ / anti-quark
    i=9
    write(14,fmt1) LHE_IDUP(i),ISTUP(i), MOTHUP(1,i),MOTHUP(2,i), ICOLUP(1,i),ICOLUP(2,i),MomDummy(2:4,5),MomDummy(1,5),L22Mass,Lifetime,Spin

! lepton 2- / quark
    i=8
    write(14,fmt1) LHE_IDUP(i),ISTUP(i), MOTHUP(1,i),MOTHUP(2,i), ICOLUP(1,i),ICOLUP(2,i),MomDummy(2:4,6),MomDummy(1,6),L21Mass,Lifetime,Spin

    write(14,"(A)") "</event>"


END SUBROUTINE



SUBROUTINE EvalPhasespace_ZDecay(ZMom,MZ,xRndPS,MomDK,PSWgt)
use ModMisc
use ModParameters
implicit none
real(8) :: PSWgt,PSWgt2,PSWgt3
real(8) :: ZMom(1:4),MomChk(1:4,1:3)
real(8) :: MomDK(1:4,1:2)
real(8) :: xRndPS(1:2),MZ
integer,parameter :: N2=2
real(8),parameter :: PiWgt2 = (2d0*Pi)**(4-N2*3) * (4d0*Pi)**(N2-1)


!     MomDK(1:4,i): i= 1:l+, 2:l-
      call genps(2,MZ,xRndPS(1:2),(/0d0,0d0/),MomDK(1:4,1:2),PSWgt2)
!     boost all guys to the Z frame:
      call boost(MomDK(1:4,1),ZMom(1:4),MZ)
      call boost(MomDK(1:4,2),ZMom(1:4),MZ)
      PSWgt = PSWgt2*PiWgt2

RETURN
END SUBROUTINE





SUBROUTINE EvalPhasespace_2to2Z(EHat,Masses,xRndPS,Mom,PSWgt)
use ModMisc
use ModParameters
implicit none
real(8) :: EHat,Masses(1:2)
real(8) :: PSWgt,PSWgt2,PSWgt3,PSWgt4,PSWgt5
real(8) :: Mom(1:4,1:4),MomW(1:4),xRndPS(1:2)
integer,parameter :: N2=2
real(8),parameter :: PiWgt2 = (2d0*Pi)**(4-N2*3) * (4d0*Pi)**(N2-1)


!  generate PS: massless + massless --> massive(anti-top) + massive(top)
   call genps(2,Ehat,xRndPS(1:2),Masses,Mom(1:4,3:4),PSWgt)
   PSWgt = PSWgt*PiWgt2

!  particles on the beam axis:
   Mom(1,1) =  EHat*0.5d0
   Mom(2,1) =  0d0
   Mom(3,1) =  0d0
   Mom(4,1) = +EHat*0.5d0

   Mom(1,2) =  EHat*0.5d0
   Mom(2,2) =  0d0
   Mom(3,2) =  0d0
   Mom(4,2) = -EHat*0.5d0

return
END SUBROUTINE




subroutine AdjustKinematics(eta1,eta2,MomExt,MomDK,xgr,xz2,xz1,MomExt_f,MomDK_f)
 use ModParameters
 use ModMisc
#if compiler==1
 use ifport
#endif
 implicit none
 real(8) :: eta1,eta2,MomExt(1:4,1:4),MomDK(1:4,1:4),xgr,xz1,xz2
 real(8) :: MomG(1:4),MomBoost(1:4),MomZ1(1:4),MomZ2(1:4)
 real(8) :: Moml1_1(1:4),Moml1_2(1:4),Moml2_1(1:4),Moml2_2(1:4)
 real(8) :: EZ,  EZ1, EZ2, pz, MZ1, MZ2,  xmax, xx1, xx2
 real(8) :: pz12, MomExt_f(1:4,1:4), MomDK_f(1:4,1:4)
 real(8) :: MZ, MG, MomG_f(1:4)

!---- summarize all the momenta / before the invariant mass adjustments

    MomZ1(1:4) = MomExt(1:4,3)
    MomZ2(1:4) = MomExt(1:4,4)

    MomG = MomZ1+MomZ2

    Moml1_1(1:4) = MomDK(1:4,1)
    Moml1_2(1:4) = MomDK(1:4,2)

    Moml2_1(1:4) = MomDK(1:4,3)
    Moml2_2(1:4) = MomDK(1:4,4)

!----- begin with the invariant mass adjustment starting from the ``Gravition''

    MomExt_f(:,:) = 0d0

    xmax = atan((Collider_Energy**2-m_Grav**2)/m_Grav/Ga_Grav) + atan(m_Grav/Ga_Grav)
    MG=dsqrt(m_Grav**2 + m_Grav*Ga_Grav*tan(xgr*xmax-atan(m_Grav/Ga_Grav)))

    if ((MG/m_Grav*eta1.gt.1).or.(MG/m_Grav*eta2.gt.1)) return

    MomExt_f(:,1) =MG/m_Grav*MomExt(:,1)
    MomExt_f(:,2) =MG/m_Grav*MomExt(:,2)

    MomG_f(1:4) = MomExt_f(1:4,1)+MomExt_f(1:4,2)


!--------------------------------------------------------

    MomBoost(1) = MomG(1)
    MomBoost(2:4) = -MomG(2:4)

    call boost(MomZ1(1:4),MomBoost(1:4),m_Grav)
    call boost(MomZ2(1:4),MomBoost(1:4),m_Grav)


 !-- energies and momenta of the Z's in Gr rest frame
     EZ = m_Grav/two
     pz = sqrt(EZ**2 - m_Z**2)

 !--- generate two more random numbers, to get invariant masses of the two Z's

    xmax = atan((mG**2-m_Z**2)/m_Z/Ga_Z) + atan(m_Z/Ga_Z)
    MZ1=dsqrt(m_Z**2 + m_Z*Ga_Z*tan(xz2*xmax-atan(m_Z/Ga_Z)))
    MZ2=dsqrt(m_Z**2 + m_Z*Ga_Z*tan(xz1*xmax-atan(m_Z/Ga_Z)))


    if (mG.lt.(MZ1 + MZ2))  return                ! reject events which can not happen

    EZ1 = (mG**2 + MZ1**2 - MZ2**2)/2d0/mG
    EZ2 = (mG**2 + MZ2**2 - MZ1**2)/2d0/mG
    pz12 = sqrt(EZ1**2 - MZ1**2)

 !-- calculating the proper Z-four vectors in the Grav rest frame

    MomZ1(1) = MomZ1(1)*EZ1/Ez
    MomZ1(2:4) = MomZ1(2:4)*pz12/pz

    MomZ2(1) = MomZ2(1)*EZ2/Ez
    MomZ2(2:4)= MomZ2(2:4)*pz12/pz



 !-- boost the new vectors into the lab frame

    call boost(MomZ1(1:4),MomG_f(1:4),mG)
    call boost(MomZ2(1:4),MomG_f(1:4),mG)


 !-- now, do the same exercise with the leptons

 !--- first Z
    MomBoost(1)   =  MomExt(1,3)
    MomBoost(2:4) = -MomExt(2:4,3)

    call boost(Moml1_1(1:4),MomBoost,m_Z)
    call boost(Moml1_2(1:4),MomBoost,m_Z)

    Moml1_1 = MZ1/m_Z*Moml1_1
    Moml1_2 = MZ1/m_Z*Moml1_2

    call boost(Moml1_1(1:4),MomZ1(1:4),mZ1)
    call boost(Moml1_2(1:4),MomZ1(1:4),mZ1)

 !-- second Z

    MomBoost(1)   =  MomExt(1,4)
    MomBoost(2:4) = -MomExt(2:4,4)

    call boost(Moml2_1(1:4),MomBoost,m_Z)
    call boost(Moml2_2(1:4),MomBoost,m_Z)

    Moml2_1 = MZ2/m_Z*Moml2_1
    Moml2_2 = MZ2/m_Z*Moml2_2

    call boost(Moml2_1(1:4),MomZ2(1:4),mZ2)
    call boost(Moml2_2(1:4),MomZ2(1:4),mZ2)


 !--- now the full collection of all 4-vectors ; with off-shell kinematics

    MomExt_f(1:4,3) = MomZ1(1:4)
    MomExt_f(1:4,4) = MomZ2(1:4)

    MomDK_f(1:4,1) = Moml1_1(1:4)
    MomDK_f(1:4,2) = Moml1_2(1:4)
    MomDK_f(1:4,3) = Moml2_1(1:4)
    MomDK_f(1:4,4) = Moml2_2(1:4)

end subroutine AdjustKinematics





SUBROUTINE Kinematics(NumPart,MomExt,MomDK,applyPSCut,NBin)
use ModMisc
use ModParameters
implicit none
real(8) :: MomExt(:,:),MomDK(:,:), m_Z1, m_Z2, MG
real(8) :: MomLepP(1:4),MomLepM(1:4),MomBoost(1:4),MomZ(1:4),MomG(1:4)
real(8) :: MomLept(1:4,1:4)
logical :: applyPSCut
integer :: NumPart,NBin(:)
real(8) :: pT_lepM,pT_lepP
real(8) :: CosPhi_LepPZ,InvM_Lep,CosPhi_LepPlanes,CosThetaZ


      applyPSCut = .false.

!--- compute the invariant mass of the ``graviton''

      mG = sqrt(2d0*(MomExt(1,1)*MomExt(1,2) - MomExt(2,1)*MomExt(2,2)   &
      - MomExt(3,1)*MomExt(3,2) - MomExt(4,1)*MomExt(4,2)))

!--- compute the invariant mass of the two pairs of leptons -- the ``Z'' masses
      m_Z1 = sqrt(2d0*(MomDK(1,1)*MomDK(1,2) - MomDK(2,1)*MomDK(2,2) &
      - MomDK(3,1)*MomDK(3,2)  - MomDK(4,1)*MomDK(4,2)))

      m_Z2 = sqrt(2d0*(MomDK(1,3)*MomDK(1,4) - MomDK(2,3)*MomDK(2,4) &
      - MomDK(3,3)*MomDK(3,4)  - MomDK(4,3)*MomDK(4,4)))


!  eval kinematic variables
!     angle
      MomBoost(1)   =+MomExt(1,3)
      MomBoost(2:4) =-MomExt(2:4,3)

      MomLepP(1:4)  = MomDK(1:4,1)
      call boost(MomLepP(1:4),MomBoost(1:4),m_Z1)

      MomZ(1:4) = MomExt(1:4,4)
      call boost(MomZ(1:4),MomBoost(1:4),m_Z1)

      CosPhi_LepPZ = (MomLepP(2)*MomZ(2)+MomLepP(3)*MomZ(3)  &
      +MomLepP(4)*MomZ(4))/MomLepP(1)/dsqrt(MomZ(1)**2-m_Z2**2)

!     pT of leptons
      pT_lepP = get_PT(MomDK(1:4,1))
      pT_lepM = get_PT(MomDK(1:4,2))

!     angle between lepton planes
!      MomLepP(2:4) = MomDK(2:4,1).cross.MomDK(2:4,2)
!      MomLepP(2:4) = MomLepP(2:4)/dsqrt( MomLepP(2)**2+MomLepP(3)**2+MomLepP(4)**2 )
!      MomLepM(2:4) = MomDK(2:4,3).cross.MomDK(2:4,4)
!      MomLepM(2:4) = MomLepM(2:4)/dsqrt( MomLepM(2)**2+MomLepM(3)**2+MomLepM(4)**2 )

      MomG(1:4)= MomExt(1:4,3) + MomExt(1:4,4)
      MomBoost(1)   =+MomG(1)
      MomBoost(2:4) =-MomG(2:4)
      MomLept = MomDK
      call boost(MomLept(1:4,1),MomBoost(1:4),mG)
      call boost(MomLept(1:4,2),MomBoost(1:4),mG)
      call boost(MomLept(1:4,3),MomBoost(1:4),mG)
      call boost(MomLept(1:4,4),MomBoost(1:4),mG)

      MomLepP(2:4) = MomLept(2:4,1).cross.MomLept(2:4,2)
      MomLepP(2:4) = MomLepP(2:4)/dsqrt( MomLepP(2)**2+MomLepP(3)**2+MomLepP(4)**2 )
      MomLepM(2:4) = MomLept(2:4,3).cross.MomLept(2:4,4)
      MomLepM(2:4) = MomLepM(2:4)/dsqrt( MomLepM(2)**2+MomLepM(3)**2+MomLepM(4)**2 )

      CosPhi_LepPlanes = acos(MomLepP(2)*MomLepM(2)+MomLepP(3)*MomLepM(3)+MomLepP(4)*MomLepM(4))

!     scattering angle of Z in graviton rest frame
      MomG(1:4)= MomExt(1:4,3) + MomExt(1:4,4)
      MomBoost(1)   =+MomG(1)
      MomBoost(2:4) =-MomG(2:4)
      MomZ(1:4) = MomExt(1:4,4)
      call boost(MomZ(1:4),MomBoost(1:4),mG)
      CosThetaZ = MomZ(4)/dsqrt(MomZ(2)**2+MomZ(3)**2+MomZ(4)**2)

!     lepton invariant mass distribuion - should be Breit-Wignher

!     binning
      NBin(1) = WhichBin(1,pT_lepP)
      NBin(2) = WhichBin(2,pT_lepM)
      NBin(3) = WhichBin(3,CosPhi_LepPZ)
      NBin(4) = WhichBin(4,CosPhi_LepPlanes)
      NBin(5) = WhichBin(5,CosThetaZ)
      NBin(6) = WhichBin(6,m_Z1)
      NBin(7) = WhichBin(7,m_Z2)
      NBin(8) = WhichBin(8,mG)

return
END SUBROUTINE


FUNCTION ZQBranching(xRnd)
use ModParameters
implicit none
real(8) :: xRnd
integer :: ZQBranching


  if( xRnd .le. Br_Z_up ) then
      ZQBranching = Up_
  elseif(xRnd .le. Br_Z_up+Br_Z_ch) then
      ZQBranching = Chm_
  elseif(xRnd .le. Br_Z_up+Br_Z_ch+Br_Z_dn) then
      ZQBranching = Dn_
  elseif(xRnd .le. Br_Z_up+Br_Z_ch+Br_Z_dn+Br_Z_st) then
      ZQBranching = Str_
  elseif(xRnd .le. Br_Z_up+Br_Z_ch+Br_Z_dn+Br_Z_st+Br_Z_bo) then
      ZQBranching = Bot_
  else
      print *, "error ",xRnd
      stop
  endif

RETURN
END FUNCTION






FUNCTION WhichBin(NHisto,Value)
implicit none
integer :: WhichBin,NHisto
real(8) :: Value

   WhichBin = (Value-Histo(NHisto)%LowVal)/Histo(NHisto)%BinSize + 1
   if( WhichBin.lt.0 ) then
      WhichBin = 0
   elseif( WhichBin.gt.Histo(NHisto)%NBins ) then
      WhichBin = Histo(NHisto)%NBins+1
   endif

RETURN
END FUNCTION





SUBROUTINE IntoHisto(NHisto,NBin,Value)
implicit none
integer :: NHisto,NBin
real(8) :: Value

     Histo(NHisto)%Value(NBin) = Histo(NHisto)%Value(NBin)  + Value
     Histo(NHisto)%Value2(NBin)= Histo(NHisto)%Value2(NBin) + Value**2
     Histo(NHisto)%Hits(NBin)  = Histo(NHisto)%Hits(NBin)+1

RETURN
END SUBROUTINE







SUBROUTINE boost2Lab(x1,x2,NumPart,Mom)
implicit none
real(8) Mom(1:4,1:NumPart)
real(8) x1,x2
real(8) gamma,betagamma,MomTmp1,MomTmp4
integer :: i,NumPart

  gamma     = (x1+x2)/2d0/dsqrt(x1*x2)
  betagamma = (x2-x1)/2d0/dsqrt(x1*x2)

  do i=1,NumPart
      MomTmp1=Mom(1,i)
      MomTmp4=Mom(4,i)
      Mom(1,i)= gamma*MomTmp1 - betagamma*MomTmp4
      Mom(4,i)= gamma*MomTmp4 - betagamma*MomTmp1
  enddo

RETURN
END SUBROUTINE




SUBROUTINE PDFMapping(MapType,yRnd,eta1,eta2,Ehat,sHatJacobi)
use ModParameters
use ModMisc
implicit none
integer :: MapType
real(8) :: yRnd(1:2),eta1,eta2,EHat,sHatJacobi,tau,nPotMap,z,sbar,fmax
real(8) :: etamin, Ymax, Y

  if( MapType.eq.1 ) then!  no mapping
      eta1 = yRnd(1)
      eta2 = yRnd(2)
      sHatJacobi = 1d0
  elseif( MapType.eq.2 ) then!  exponential mapping
!       tau = (2d0*m_Top/Collider_Energy)**2
!       eta1 = tau**yRnd(1)
!       eta2 = tau**( (1d0-yRnd(1))*yRnd(2) )
!       sHatJacobi = dlog(tau)**2*(1d0-yRnd(1))*eta1*eta2
  elseif( MapType.eq.3 ) then!  linear mapping
!       tau = (2d0*m_Top/Collider_Energy)**2
!       eta1 = (1d0-tau)*yRnd(1) + tau
!       eta2 = ((1d0-tau)*yRnd(1))/((1d0-tau)*yRnd(1)+tau)*yRnd(2) + tau/((1d0-tau)*yRnd(1)+tau)
!       sHatJacobi = (1d0-tau)*((1d0-tau)*yRnd(1))/((1d0-tau)*yRnd(1)+tau)
  elseif( MapType.eq.4 ) then!  MCFM mapping
!       tau = dexp(dlog(((2d0*m_Top/Collider_Energy)**2))*yRnd(1))
!       eta1 = dsqrt(tau)*dexp(0.5d0*dlog(tau)*(1d0-2d0*yRnd(2)))
!       eta2 = dsqrt(tau)/dexp(0.5d0*dlog(tau)*(1d0-2d0*yRnd(2)))
!       sHatJacobi = dlog(((2d0*m_Top/Collider_Energy)**2))*tau*dlog(tau)
  elseif( MapType.eq.5 ) then!  nPotMap mapping
!       nPotMap = 0.5d0
!       tau = (2d0*m_Top/Collider_Energy)**2
!       yRnd(1) = yRnd(1)**nPotMap
!       yRnd(2) = yRnd(2)**nPotMap
!       eta1 = (1d0-tau) * yRnd(1) + tau
!       eta2 = ((1d0-tau)*yRnd(1))/((1d0-tau)*yRnd(1)+tau)*yRnd(2) + tau/((1d0-tau)*yRnd(1)+tau)
!       sHatJacobi=(1d0-tau)*((1d0-tau)*yRnd(1))/((1d0-tau)*yRnd(1)+tau)*nPotMap**2*((yRnd(1)*yRnd(2))**(1d0/nPotMap))**(nPotMap-1d0)
  elseif( MapType.eq.10 ) then!  Breit-Wigner mapping
      fmax = 1d0/m_Grav/Ga_Grav * ( datan((Collider_Energy**2-m_Grav**2)/m_Grav/Ga_Grav) - datan(-m_Grav/Ga_Grav) )
      sbar = m_Grav*Ga_Grav * dtan(fmax*yRnd(1)*m_Grav*Ga_Grav - datan(m_Grav/Ga_Grav) ) + m_Grav**2
      z = sbar/Collider_Energy**2
      eta1 = z + (1d0-z)*yRnd(2)
      eta2 = z/eta1
      sHatJacobi = fmax/Collider_Energy**2 * (1d0-z)/eta1  * ( (sbar - m_Grav**2)**2 + m_Grav**2*Ga_Grav**2 )
  elseif (MapType.eq.11) then ! delta-function map

     etamin = m_Grav**2/Collider_Energy**2
     eta2 = etamin + (1d0-etamin)*yRnd(2)
     eta1 = etamin/eta2
     fmax = 0.5d0*pi/m_Grav**3/Ga_Grav
     sHatJacobi = fmax*etamin/eta2* ( (Collider_Energy**2*eta1*eta2 - m_Grav**2)**2 + m_Grav**2*Ga_Grav**2 )

  elseif (MapType.eq.12) then ! delta-function map / new
     Ymax = log(Collider_Energy/m_Grav)
     Y = -Ymax + 2d0*Ymax*yRnd(2)
     eta1 = m_Grav/Collider_Energy*exp(Y)
     eta2 = m_Grav/Collider_Energy*exp(-Y)
     fmax = 0.5d0*pi/m_Grav**3/Ga_Grav*2d0*Ymax
     sHatJacobi = fmax*(m_Grav**2*Ga_Grav**2 )
  else
      call Error("PDF mapping not available")
  endif

  EHat = Collider_Energy*dsqrt(eta1*eta2)

RETURN
END SUBROUTINE







SUBROUTINE setPDFs(x1,x2,MuFac,pdf)
use ModParameters
implicit none
real(8) :: x1,x2,PDFScale,MuFac
real(8) :: upv(1:2),dnv(1:2),usea(1:2),dsea(1:2),str(1:2),chm(1:2),bot(1:2),glu(1:2),phot(1:2),sbar(1:2),cbar(1:2),bbar(1:2)
integer,parameter :: swPDF_u=1, swPDF_d=1, swPDF_c=1, swPDF_s=1, swPDF_b=1, swPDF_g=1
real(8) :: pdf(-6:6,1:2)

        PDFScale=MuFac*100d0
        if( PDFSet.eq.1 ) then
            call cteq6(x1,PDFScale,upv(1),dnv(1),usea(1),dsea(1),str(1),chm(1),bot(1),glu(1))
            call cteq6(x2,PDFScale,upv(2),dnv(2),usea(2),dsea(2),str(2),chm(2),bot(2),glu(2))
        elseif( PDFSet.eq.2 ) then
            call GetAllPDFs("pdfs/mstw2008lo",0,x1,PDFScale,upv(1),dnv(1),usea(1),dsea(1),str(1),sbar(1),chm(1),cbar(1),bot(1),bbar(1),glu(1),phot(1))
            str(1)= (str(1)+sbar(1))/2d0
            chm(1)= (chm(1)+cbar(1))/2d0
            bot(1)= (bot(1)+bbar(1))/2d0
            upv(1)=upv(1)/x1
            dnv(1)=dnv(1)/x1
            usea(1)=usea(1)/x1
            dsea(1)=dsea(1)/x1
            str(1)=str(1)/x1
            chm(1)=chm(1)/x1
            bot(1)=bot(1)/x1
            glu(1)=glu(1)/x1
            phot(1)=phot(1)/x1

            call GetAllPDFs("pdfs/mstw2008lo",0,x2,PDFScale,upv(2),dnv(2),usea(2),dsea(2),str(2),sbar(2),chm(2),cbar(2),bot(2),bbar(2),glu(2),phot(2))
            str(2)= (str(2)+sbar(2))/2d0
            chm(2)= (chm(2)+cbar(2))/2d0
            bot(2)= (bot(2)+bbar(2))/2d0
            upv(2)=upv(2)/x2
            dnv(2)=dnv(2)/x2
            usea(2)=usea(2)/x2
            dsea(2)=dsea(2)/x2
            str(2)=str(2)/x2
            chm(2)=chm(2)/x2
            bot(2)=bot(2)/x2
            glu(2)=glu(2)/x2
            phot(2)=phot(2)/x2

        elseif( PDFSet.ge.201 .and. PDFSet.le.240) then
            call GetAllPDFs("pdfs/mstw2008lo.90cl",PDFSet-200,x1,PDFScale,upv(1),dnv(1),usea(1),dsea(1),str(1),sbar(1),chm(1),cbar(1),bot(1),bbar(1),glu(1),phot(1))
            str(1)= (str(1)+sbar(1))/2d0
            chm(1)= (chm(1)+cbar(1))/2d0
            bot(1)= (bot(1)+bbar(1))/2d0
            upv(1)=upv(1)/x1
            dnv(1)=dnv(1)/x1
            usea(1)=usea(1)/x1
            dsea(1)=dsea(1)/x1
            str(1)=str(1)/x1
            chm(1)=chm(1)/x1
            bot(1)=bot(1)/x1
            glu(1)=glu(1)/x1
            phot(1)=phot(1)/x1

            call GetAllPDFs("pdfs/mstw2008lo.90cl",PDFSet-200,x2,PDFScale,upv(2),dnv(2),usea(2),dsea(2),str(2),sbar(2),chm(2),cbar(2),bot(2),bbar(2),glu(2),phot(2))
            str(2)= (str(2)+sbar(2))/2d0
            chm(2)= (chm(2)+cbar(2))/2d0
            bot(2)= (bot(2)+bbar(2))/2d0
            upv(2)=upv(2)/x2
            dnv(2)=dnv(2)/x2
            usea(2)=usea(2)/x2
            dsea(2)=dsea(2)/x2
            str(2)=str(2)/x2
            chm(2)=chm(2)/x2
            bot(2)=bot(2)/x2
            glu(2)=glu(2)/x2
            phot(2)=phot(2)/x2
        else
            print *, "PDFSet",PDFSet,"not available!"
            stop
        endif

IF( COLLIDER.EQ.1 ) THEN
!       PROTON CONTENT
        pdf(Up_,1)   = (upv(1) + usea(1))  * swPDF_u
        pdf(AUp_,1)  = usea(1)             * swPDF_u
        pdf(Dn_,1)   = (dnv(1) + dsea(1))  * swPDF_d
        pdf(ADn_,1)  = dsea(1)             * swPDF_d
        pdf(Chm_,1)  = chm(1)              * swPDF_c
        pdf(AChm_,1) = chm(1)              * swPDF_c
        pdf(Str_,1)  = str(1)              * swPDF_s
        pdf(AStr_,1) = str(1)              * swPDF_s
        pdf(Bot_,1)  = bot(1)              * swPDF_b
        pdf(ABot_,1) = bot(1)              * swPDF_b
        pdf(0,1)     = glu(1)              * swPDF_g

!       PROTON CONTENT
        pdf(Up_,2)   = (upv(2) + usea(2))  * swPDF_u
        pdf(AUp_,2)  = usea(2)             * swPDF_u
        pdf(Dn_,2)   = (dnv(2) + dsea(2))  * swPDF_d
        pdf(ADn_,2)  = dsea(2)             * swPDF_d
        pdf(Chm_,2)  = chm(2)              * swPDF_c
        pdf(AChm_,2) = chm(2)              * swPDF_c
        pdf(Str_,2)  = str(2)              * swPDF_s
        pdf(AStr_,2) = str(2)              * swPDF_s
        pdf(Bot_,2)  = bot(2)              * swPDF_b
        pdf(ABot_,2) = bot(2)              * swPDF_b
        pdf(0,2)     = glu(2)              * swPDF_g

ELSEIF( COLLIDER.EQ.2 ) THEN
!       PROTON CONTENT
        pdf(Up_,1)   = (upv(1) + usea(1))  * swPDF_u
        pdf(AUp_,1)  = usea(1)             * swPDF_u
        pdf(Dn_,1)   = (dnv(1) + dsea(1))  * swPDF_d
        pdf(ADn_,1)  = dsea(1)             * swPDF_d
        pdf(Chm_,1)  = chm(1)              * swPDF_c
        pdf(AChm_,1) = chm(1)              * swPDF_c
        pdf(Str_,1)  = str(1)              * swPDF_s
        pdf(AStr_,1) = str(1)              * swPDF_s
        pdf(Bot_,1)  = bot(1)              * swPDF_b
        pdf(ABot_,1) = bot(1)              * swPDF_b
        pdf(0,1)     = glu(1)              * swPDF_g

!       ANTI-PROTON CONTENT
        pdf(Up_,2)   = usea(2)             * swPDF_u
        pdf(AUp_,2)  = (upv(2)+usea(2))    * swPDF_u
        pdf(Dn_,2)   = dsea(2)             * swPDF_d
        pdf(ADn_,2)  = (dnv(2) + dsea(2))  * swPDF_d
        pdf(Chm_,2)  = chm(2)              * swPDF_c
        pdf(AChm_,2) = chm(2)              * swPDF_c
        pdf(Str_,2)  = str(2)              * swPDF_s
        pdf(AStr_,2) = str(2)              * swPDF_s
        pdf(Bot_,2)  = bot(2)              * swPDF_b
        pdf(ABot_,2) = bot(2)              * swPDF_b
        pdf(0,2)     = glu(2)              * swPDF_g
ENDIF

RETURN
END SUBROUTINE



SUBROUTINE CTEQ6(X,SCALE,UPV,DNV,USEA,DSEA,STR,CHM,BOT,GLU)
implicit none
double precision X,SCALE,UPV,DNV,USEA,DSEA,STR,CHM,BOT,GLU
double precision Q,xsave,qsave,Ctq6Pdf,D,U

         Q=SCALE
         xsave=X
         qsave=Q
         U =         Ctq6Pdf(1,X,Q)
         D =         Ctq6Pdf(2,X,Q)
         USEA =      Ctq6Pdf(-1,X,Q)
         DSEA =      Ctq6Pdf(-2,X,Q)
         STR =       Ctq6Pdf(3,X,Q)
         CHM =       Ctq6Pdf(4,X,Q)
         BOT =       Ctq6Pdf(5,X,Q)
         GLU  =      Ctq6Pdf(0,X,Q)
         UPV=U-USEA
         DNV=D-DSEA
         X=xsave
         Q=qsave
RETURN
END SUBROUTINE



END MODULE
