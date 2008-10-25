C*********************************************************************
C   PROGRAM    :    SHALXY
C   LANGUAGE   :    MS FORTRAN 5.0
C   DESIGNED BY:    R. M. AUNE
C   PURPOSE    :    2-D SHALLOW WATER MODEL
C   HISTORY    :    CODED                  NOV 81
C                   RESTRUCTURED           DEC 87
C                   COPIED FROM VRAUSHXY   SEP 89
C                   MS FORT 5.0            JUN 90
C                   3D GRAPHICS            OCT 91
C                   USER MENU              JUN 92
C
C   DESCRIPTION:    THIS PROGRAM UTILIZES THE TWO DIMENSIONAL SHALLOW
C                   FLUID EQUATIONS TO ANALYZE VARIOUS DYNAMIC AND
C                   COMPUTATIONAL PROBLEMS THAT ARRISE IN NUMERICAL
C                   WEATHER PREDICTION. THIS VERSION DISPLAYS TWO
C                   WINDOWS: SFC RENDER AND CONTOUR/VECTORS.
C
C   INPUT DATA:
C      NMAX            - TOTAL TIMESTEPS
C      NOUT            - OUTPUT INTERVAL
C      DELT DELX       - TIMESTEP (SEC), GRID INTERVAL (M)
C      UBAR VBAR HBAR  - MEAN U AND V (M/S), MEAN HEIGHT (M)
C      IDIFU           - 0 = NO U,V DIFFUSION; 1 = U,V DIFFUSION
C      IDIFH           - 0 = NO HEIGHT DIFFUSION; 1 = HEIGHT DIFF
C      ADIFF           - INTERIOR DIFFUSION COEFFICIENT
C      IORD            - 4 = 4TH ORDER DIFF
C      G               - = 9.80616, OR 0. FOR NO G TERM
C      ALAT            - LAT OF SOUTH BNDRY, OR 0 FOR NO CORIOLIS
C
C   FEATURES   :    THREE OPTIONS ARE AVAILABLE FOR AN INITIAL HEIGHT
C                   FIELD: SQUARE WAVE, SINE WAVE, OR PYRAMID.
C                   THE CFL STABILITY COMPUTED AND TESTED
C                   BASED ON THE CHOSEN MODEL CONFIGURATION
C*********************************************************************
C
C      SUBROUTINE SHALSTEP
      SUBROUTINE SHALSTEP(NSTEP, U11, V11, H11, CC11,
     *                    U12, V12, H12, CC12, U13, V13, H13, CC13,
     *                    IOPT, IBC, G, ALAT, UBAR1, VBAR1,
     *                    HPRM1, HPRM2, DELT_COPY, EPS, ADIFF, TFILT)

      INCLUDE "shsize.fcm"

       REAL U11(NX,NY), V11(NX,NY), H11(NX,NY), CC11(NX,NY)
       REAL U12(NX,NY), V12(NX,NY), H12(NX,NY), CC12(NX,NY)
       REAL U13(NX,NY), V13(NX,NY), H13(NX,NY), CC13(NX,NY)

      REAL U1(NX,NY,3),V1(NX,NY,3),H1(NX,NY,3),CC1(NX,NY,3)
     &    ,UBAR1,VBAR1,HBAR1,HPRM1(2)
C     REAL U2(NX,NY,3),V2(NX,NY,3),H2(NX,NY,3),CC2(NX,NY,3)
C    &    ,UBAR2,VBAR2,HBAR2,HPRM2(2)
C     REAL U3(NX,NY),V3(NX,NY),H3(NX,NY),CC3(NX,NY)
C    &    ,UBAR3,VBAR3,HBAR3,HPRM3(2)
      REAL DUDX(NX,NY),DVDX(NX,NY),DHDX(NX,NY)
     &     ,DUDY(NX,NY),DVDY(NX,NY),DHDY(NX,NY)
     &     ,DCCDX(NX,NY),DCCDY(NX,NY)
     &     ,DKU(NX,NY),DKV(NX,NY),DKH(NX,NY),DKC(NX,NY)
C     REAL F(NY),DIFF(NX,NY)
      REAL F(NY)
      COMMON/SCALAR/DELX,DELT,DELT2,OV12DX,OV2DX,OVDX2
     &             ,NXM1,NXM2,NXM3,NXM4,NXM5,NXM6
     &             ,NYM1,NYM2,NYM3,NYM4,NYM5,NYM6
     &             ,I1,I2,I3,I4,I5,J1,J2,J3,J4,J5
C     LOGICAL LTFLT
      INTEGER ADINT
      CHARACTER*1 CODE(16),OPCODE,YUP,NOP,ANS
      CHARACTER*6 INCON(5),DTYP(3)
      CHARACTER*7 BCTYP(3)
      logical first/.true./
      integer openw
      integer*2 npixx,npixy
      character*60 wlabel
      INTEGER*2 MINX,MINY,MAXX,MAXY
      COMMON/SCREEN2/MINX,MINY,MAXX,MAXY
C
c     DATA YUP,NOP/'Y','N'/
c     DATA CODE/'I','B','G','C','W','H','N','O','T','M','Z','S','R'
c    &         ,'Q',2*' '/
      DATA YUP,NOP/'y','n'/
      DATA CODE/'i','b','g','c','w','h','n','o','t','m','f','s','r'
     &         ,'q',2*' '/
C      DATA NSTEP,NALT/0,0/
      DATA NALT/0/
      DATA PI/3.14159/
      DATA STAB/.73/
      DATA DTYP/' NONE ','2NDDIF','TANFLT'/
      DATA INCON/'WAVE  ','MOUNT ','VORTEX','STEP  ','DUAL V'/
      DATA BCTYP/'CYCLIC ','REFLEX ','CHANNEL'/

       DO 10 I=1,NX
       DO 10 J=1,NY
       U1(I, J, 1) = U11(I, J)
       V1(I, J, 1) = V11(I, J)
       H1(I, J, 1) = H11(I, J)
       CC1(I, J, 1) = CC11(I, J)
       U1(I, J, 2) = U12(I, J)
       V1(I, J, 2) = V12(I, J)
       H1(I, J, 2) = H12(I, J)
       CC1(I, J, 2) = CC12(I, J)
       U1(I, J, 3) = U13(I, J)
       V1(I, J, 3) = V13(I, J)
       H1(I, J, 3) = H13(I, J)
       CC1(I, J, 3) = CC13(I, J)
10     CONTINUE
       DELT = DELT_COPY

C       WRITE (6, *) IOPT, IBC, G, ALAT

C
C      NSTEP = ADINT(1)
C      CALL ADM2D(2, 1, NX*NY, U1(1,1,1), MY, MX)
C      CALL ADM2D(2, 2, NX*NY, V1(1,1,1), MY, MX)
C      CALL ADM2D(2, 3, NX*NY, H1(1,1,1), MY, MX)
C      CALL ADM2D(2, 4, NX*NY, CC1(1,1,1), MY, MX)
C      CALL ADM2D(3, 1, NX*NY, U1(1,1,2), MY, MX)
C      CALL ADM2D(3, 2, NX*NY, V1(1,1,2), MY, MX)
C      CALL ADM2D(3, 3, NX*NY, H1(1,1,2), MY, MX)
C      CALL ADM2D(3, 4, NX*NY, CC1(1,1,2), MY, MX)
C      CALL ADM2D(4, 1, NX*NY, U1(1,1,3), MY, MX)
C      CALL ADM2D(4, 2, NX*NY, V1(1,1,3), MY, MX)
C      CALL ADM2D(4, 3, NX*NY, H1(1,1,3), MY, MX)
C      CALL ADM2D(4, 4, NX*NY, CC1(1,1,3), MY, MX)
C      IOPT = ADINT(5)
C      IBC = ADINT(6)
C      G = ADREAL(7)
C      ALAT = ADREAL(8)
C      UBAR1 = ADREAL(9)
C      VBAR1 = ADREAL(10)
C      HPRM1(1) = ADREAL(11)
C      HPRM1(2) = ADREAL(12)
C      DELT = ADREAL(13)
C      EPS = ADREAL(14)
C      ADIFF = ADREAL(15)
C      TFILT = ADREAL(16)

C---INITIAL CONFIGURATION
      DELX = 150000.
C     IOPT=2
C     IBC=3
C     G=9.80616
C     ALAT=0.
      IF(ALAT.EQ.0.)THEN
         DO 3 J=1,NY
 3       F(J)=0.
      ELSE
         TLAT=ALAT
         DLAT=DELX/111000.
         F(1)=2.*7.292E-5*SIN(TLAT*PI/180.)
         DO 4 J=2,NY
            TLAT=TLAT+DLAT
            F(J)=2.*7.292E-5*SIN(TLAT*PI/180.)
 4       CONTINUE
      ENDIF
C     UBAR1=0.
C     VBAR1=0.
      HBAR1=5600.
C     HPRM1(1)=100.
C     HPRM1(2)=100.
      ASEP=7.
C     NMAX=15
C     NOUT=1
C     DELT=320.
C     DELTS=252.
C     ADIFF=0.
C     IDIF=0
C     TFILT=0.
      TFILTM=(1.-TFILT)/2.
C     LTFLT=.FALSE.
C     NOPT=1
C     HPRM3(1)=5.
C     HPRM3(2)=5.
C
C
C---START RUN
C 130  NSTEP=0
      CALL INIT(NSTEP,DKU,DKV,DKH,NX,NY)
C
      IF (NSTEP .EQ. 0) THEN
        CALL MAKDAT(U1,V1,H1,CC1,F,NX,NY,
     & UBAR1,VBAR1,HBAR1,HPRM1,G,IOPT,ASEP)
C        CALL ADRM2D(2, 1, U1(1,1,3), MY, MX)
C        CALL ADRM2D(2, 2, V1(1,1,3), MY, MX)
C        CALL ADRM2D(2, 3, H1(1,1,3), MY, MX)
C        CALL ADRM2D(2, 4, CC1(1,1,3), MY, MX)
       DO 20 I=1,NX
       DO 20 J=1,NY
       U13(I, J) = U1(I, J, 3)
       V13(I, J) = V1(I, J, 3)
       H13(I, J) = H1(I, J, 3)
       CC13(I, J) = CC1(I, J, 3)
20     CONTINUE
        return
      ENDIF

C     CALL MAKDAT(U2,V2,H2,CC2,F,NX,NY,UBAR1,VBAR1,HBAR1
C    &                 ,HPRM1,G,IOPT,ASEP)
C     DO 150 J=1,NY
C     DO 150 I=1,NX
C        U3(I,J)=0.
C        V3(I,J)=0.
C        H3(I,J)=0.
C        CC3(I,J)=0.
C150  CONTINUE
C
C
C---TIMESTEP LOOP
C      NSTEP=0
C first time step if half step for leap frog scheme
      IF (NSTEP .EQ. 1) DELT2=DELT2*.5
C 200  NSTEP=NSTEP+1
C
C---FORECAST A
C   COMPUTE SPACE DERIVATIVES
      CALL X1DER4(U1(1,1,2),DUDX,DUDY,NX,NY)
      CALL X1DER4(V1(1,1,2),DVDX,DVDY,NX,NY)
      CALL X1DER4(H1(1,1,2),DHDX,DHDY,NX,NY)
      CALL X1DER4(CC1(1,1,2),DCCDX,DCCDY,NX,NY)
      IF(ADIFF.GT.0.)THEN
         CALL KDIFF(U1(1,1,2),ADIFF,NX,DKU)
         CALL KDIFF(V1(1,1,2),ADIFF,NX,DKV)
         CALL KDIFF(H1(1,1,2),ADIFF,NX,DKH)
         CALL KDIFF(CC1(1,1,2),ADIFF,NX,DKC)
      ENDIF
C
C---BIT/CIS, (LEAPFROG)
      CALL CITCIS(U1,V1,H1,CC1,DUDX,DVDX,DHDX,DUDY,DVDY
     &           ,DHDY,DKU,DKV,DKH,DCCDX,DCCDY,F
     &           ,NX,NY,G)
C
C---BOUNDARY CONDITION UPDATE
      IF(IBC.EQ.1)CALL CYCLIC(U1,V1,H1,CC1,NX,NY)
      IF(IBC.EQ.2)CALL RFLCTN(U1,V1,H1,CC1,NX,NY)
      IF(IBC.EQ.3)CALL CHANEL(U1,V1,H1,CC1,NX,NY)
C
C---SPACE FILTER
      IF(EPS.GT.0.)THEN
         CALL TANFLT(U1(1,1,3),EPS,NX,NY)
         CALL TANFLT(V1(1,1,3),EPS,NX,NY)
         CALL TANFLT(H1(1,1,3),EPS,NX,NY)
         CALL TANFLT(CC1(1,1,3),EPS,NX,NY)
      ENDIF
C
C---TIME FILTER
      IF(TFILT.GT.0.)THEN
         CALL ASFILT(U1,V1,H1,CC1,NX,NY,TFILT,TFILTM)
      ENDIF
C
C---RESET FOR NEXT TIMESTEP
C      CALL SWITCH(U1,V1,H1,CC1,NX,NY)
C
C---FORECAST B
C   COMPUTE SPACE DERIVATIVES
C     CALL X1DER4(U2(1,1,2),DUDX,DUDY,NX,NY)
C     CALL X1DER4(V2(1,1,2),DVDX,DVDY,NX,NY)
C     CALL X1DER4(H2(1,1,2),DHDX,DHDY,NX,NY)
C     CALL X1DER4(CC2(1,1,2),DCCDX,DCCDY,NX,NY)
C     IF(IDIF.EQ.1)THEN
C        CALL KDIFF(U2(1,1,2),DIFF,NX,DKU)
C        CALL KDIFF(V2(1,1,2),DIFF,NX,DKV)
C        CALL KDIFF(H2(1,1,2),DIFF,NX,DKH)
C        CALL KDIFF(CC1(1,1,2),DIFF,NX,DKC)
C     ENDIF
C
C---BIT/CIS, (LEAPFROG)
C     CALL CITCIS(U2,V2,H2,CC2,DUDX,DVDX,DHDX,DUDY,DVDY
C    &           ,DHDY,DKU,DKV,DKH,DCCDX,DCCDY,DIFF,F
C    &           ,NX,NY,G)
C
C---BOUNDARY CONDITION UPDATE
C     IF(IBC.EQ.1)CALL CYCLIC(U2,V2,H2,CC2,NX,NY)
C     IF(IBC.EQ.2)CALL RFLCTN(U2,V2,H2,CC2,NX,NY)
C     IF(IBC.EQ.3)CALL CHANEL(U2,V2,H2,CC2,NX,NY)
C
C---SPACE FILTER
C     IF(IDIF.EQ.2)THEN
C        CALL TANFLT(U2(1,1,3),ADIFF,NX,NY)
C        CALL TANFLT(V2(1,1,3),ADIFF,NX,NY)
C        CALL TANFLT(H2(1,1,3),ADIFF,NX,NY)
CCC      CALL TANFLT(CC2(1,1,3),ADIFF,NX,NY)
C     ENDIF
C
C---TIME FILTER
C     IF(LTFLT)CALL ASFILT(U2,V2,H2,CC2,NX,NY,TFILT,TFILTM)
C
C---RESET FOR NEXT TIMESTEP
C     CALL SWITCH(U2,V2,H2,CC2,NX,NY)
C
      IF(NSTEP.EQ.1)DELT2=DELT2*2.
C
C---DIFFERENCE FORECASTS
C     DO 210 J=1,NY
C     DO 210 I=1,NX
C        U3(I,J)=U2(I,J,3)-U1(I,J,3)
C        V3(I,J)=V2(I,J,3)-V1(I,J,3)
C        H3(I,J)=H2(I,J,3)-H1(I,J,3)
C        CC3(I,J)=CC2(I,J,3)-CC1(I,J,3)
C210  CONTINUE
C
C---OUTPUT TO DISPLAY
C      IF(NSTEP.EQ.NMAX)GOTO 202
C      GOTO 200
C
C
C      CALL ADRM2D(2, 1, U1(1,1,3), MY, MX)
C      CALL ADRM2D(2, 2, V1(1,1,3), MY, MX)
C      CALL ADRM2D(2, 3, H1(1,1,3), MY, MX)
C      CALL ADRM2D(2, 4, CC1(1,1,3), MY, MX)
       DO 30 I=1,NX
       DO 30 J=1,NY
       U13(I, J) = U1(I, J, 3)
       V13(I, J) = V1(I, J, 3)
       H13(I, J) = H1(I, J, 3)
       CC13(I, J) = CC1(I, J, 3)
30     CONTINUE
      return
      END

