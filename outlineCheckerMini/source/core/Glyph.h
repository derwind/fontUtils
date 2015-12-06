#include "Contour.h"
#include <list>

namespace outlinecheck {

class Glyph {
 public:
	Glyph();
	~Glyph();

	void addContour(Contour& contour);

 private:
	typedef std::list<Contour*>::iterator CONTOUR_ITERATOR;

 private:
	 std::list<Contour*> mContours;
};

}	// namespace outlinecheck
