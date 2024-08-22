from RobotFrameworkBasic import RobotFrameworkBasic, robot_log_keyword, always_true_until_check


class RF(RobotFrameworkBasic):
    count_true_count_false = 5
    count_false_count_true = 5
    count_true_count_error = 5
    count_false_count_error = 5

    @robot_log_keyword
    def always_true(self):
        return True

    @robot_log_keyword
    def always_false(self):
        return False

    @robot_log_keyword
    def true_count_false(self):
        self.count_true_count_false -= 1
        return self.count_true_count_false > 0

    @robot_log_keyword
    def false_count_true(self):
        self.count_false_count_true -= 1
        return self.count_false_count_true <= 0

    @robot_log_keyword
    def true_count_error(self):
        self.count_true_count_error -= 1
        if self.count_true_count_error > 0:
            return True
        else:
            raise Exception(self.count_true_count_error)

    @robot_log_keyword
    def false_count_error(self):
        self.count_false_count_error -= 1
        if self.count_false_count_error > 0:
            return False
        else:
            raise Exception(self.count_false_count_error)

    @always_true_until_check(always_true, always_false)
    def always_true_and_always_false(self):
        pass

    @always_true_until_check(always_true, false_count_true)
    def always_true_and_false_count_true(self):
        pass

    @always_true_until_check(true_count_false, always_false)
    def true_count_false_and_always_false(self):
        pass

    @always_true_until_check(always_true, false_count_error)
    def always_true_and_false_count_error(self):
        pass

    @always_true_until_check(true_count_error, always_false)
    def true_count_error_and_always_false(self):
        pass


class Test_function_always_true_until_check:
    def test_01_pass(self):
        rf = RF()
        assert rf.always_true_and_false_count_true() is True

    def test_02_01_timeout_fail_error(self):
        rf = RF()
        try:
            rf.always_true_and_always_false(timeout=1)
        except Exception as err:
            assert isinstance(err, AssertionError)
        else:
            raise AssertionError('no error raised')

    def test_02_02_timeout_fail_false(self):
        rf = RF()
        assert rf.always_true_and_always_false(timeout=1, error=False) is False

    def test_03_01_do_fail_error(self):
        rf = RF()
        try:
            rf.true_count_false_and_always_false(timeout=1)
        except Exception as err:
            assert isinstance(err, AssertionError)
        else:
            raise AssertionError('no error raised')

    def test_03_02_do_fail_false(self):
        rf = RF()
        assert rf.true_count_false_and_always_false(timeout=1, error=False) is False

    def test_04_01_do_error_error(self):
        rf = RF()
        try:
            rf.true_count_error_and_always_false(timeout=1)
        except Exception as err:
            assert isinstance(err, AssertionError)
        else:
            raise AssertionError('no error raised')

    def test_04_02_do_error_false(self):
        rf = RF()
        assert rf.true_count_error_and_always_false(timeout=1, error=False) is False

    def test_05_01_check_error_error(self):
        rf = RF()
        try:
            rf.always_true_and_false_count_error(timeout=1)
        except Exception as err:
            assert isinstance(err, AssertionError)
        else:
            raise AssertionError('no error raised')

    def test_05_02_check_error_false(self):
        rf = RF()
        assert rf.always_true_and_false_count_error(timeout=1, error=False) is False
