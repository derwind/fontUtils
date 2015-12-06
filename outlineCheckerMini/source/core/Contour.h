namespace outlinecheck {

class Contour {
 public:
	Contour();
	Contour(const Contour &obj);

	~Contour();

	inline bool isCopied() const { return mCopied; }

 private:
	bool mCopied;
};

}	// namespace outlinecheck
