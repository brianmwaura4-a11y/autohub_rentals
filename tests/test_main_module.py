import runpy


def test_main_module_calls_main(monkeypatch):
    calls = []

    def fake_main():
        calls.append(True)

    import car_rental.cli.main

    monkeypatch.setattr(
        car_rental.cli.main,
        "main",
        fake_main
    )

    runpy.run_module(
        "car_rental.__main__",
        run_name="__main__"
    )

    assert calls == [True]
