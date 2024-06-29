import msim.helpers as mHelp

class Test_isMsimNumType:
    def setup_class(self):
        # Class setup:
        pass

    def teardown_class(self):
        # Class teardown:
        pass

    def setup(self):
        # Method setup:
        pass

    def teardown(self):
        # Method teardown:
        pass

    def test_bool(self):
        result = mHelp.isMsimNumType(bool)
        assert result

    def test_int(self):
        result = mHelp.isMsimNumType(int)
        assert result

    def test_float(self):
        result = mHelp.isMsimNumType(float)
        assert result

    def test_str(self):
        result = mHelp.isMsimNumType(str)
        assert not result
