#include "Contour.h"
#include <iostream>

using namespace outlinecheck;

Contour::Contour()
:
mCopied(false)
{
	std::cout << "A Contour object is constructed." << std::endl;
}

Contour::Contour(const Contour &obj)
:
mCopied(true)
{
	std::cout << "A Contour object is constructed via copy-constructor." << std::endl;
}

Contour::~Contour()
{
	std::cout << "A Contour object is destructed. (" << mCopied << ")" << std::endl;
}
