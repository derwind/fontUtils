#include <boost/python.hpp>
#include "Glyph.h"

BOOST_PYTHON_MODULE(outlineCheckCore)
{
	using namespace boost::python;

	class_<outlinecheck::Contour>("Contour")
	;

	class_<outlinecheck::Glyph>("Glyph")
		.def("addContour", &outlinecheck::Glyph::addContour)
	;
}


/*
int main(void)
{
	puts("hello");

	outlinecheck::Glyph g;
	outlinecheck::Contour con;
	g.addContour(con);

	return 0;
}
*/
