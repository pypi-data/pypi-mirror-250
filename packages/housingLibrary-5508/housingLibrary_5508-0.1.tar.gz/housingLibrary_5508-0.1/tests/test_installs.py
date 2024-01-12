def test_installation():
    # Check if the required packages are installed
    packages = ["pandas", "numpy", "sklearn"]
    missing_packages = []
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("Some required packages are missing:")
        for package in missing_packages:
            print(package)
    else:
        print("Installation test completed successfully!")


if __name__ == "__main__":
    test_installation()
