// Copyright 2006-2007 Nanorex, Inc.  See LICENSE file for details. 
/* $Id: W15.h,v 1.3 2007/05/17 18:16:14 emessick Exp $ */

#ifndef W15_H_INCLUDED
#define W15_H_INCLUDED

#include "W1.h"

class W15: public W1
{
 public:
    W15(int a, int b, double c, int nshells, double sshell, int terminator);
};

#endif