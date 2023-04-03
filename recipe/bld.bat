
:: set GEOS_LIBRARY_PATH=%LIBRARY_BIN%

del /f shapely\speedups\_speedups.c
del /f shapely\vectorized\_vectorized.c

"%PYTHON%" -m pip install . -vv ^
    --no-deps --ignore-installed --no-use-pep517 ^
    --global-option=build_ext ^
    --global-option="-I%LIBRARY_INC%" ^
    --global-option="-L%LIBRARY_LIB%" ^
    --global-option="-lgeos_c"
if errorlevel 1 exit 1
