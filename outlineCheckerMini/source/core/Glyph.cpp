#include "Glyph.h"
#include <iostream>

using namespace outlinecheck;

Glyph::Glyph()
{
}

Glyph::~Glyph()
{
	CONTOUR_ITERATOR it;
	for (it = mContours.begin(); it != mContours.end(); ++it) {
		std::cout << "Now delete contour (" << (*it)->isCopied() << ")" << std::endl;
		delete *it;
	}

	std::cout << "A Glyph object is destructed." << std::endl;
}

void Glyph::addContour(Contour& contour)
{
	mContours.push_back( new Contour(contour) );
}
