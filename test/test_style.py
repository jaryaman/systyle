from systyle import Style


class TestStyle:
    def test_style(self):
        style = Style.from_default()
        style.apply()
