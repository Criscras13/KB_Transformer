@echo off
echo ===================================================
echo KB_Transformer Local Data Update (No Docker)
echo ===================================================
echo.

echo [Step 1/2] Fetching data from KnowBe4 API...
python data_transformer.py
if %errorlevel% neq 0 (
    echo ERROR: Data fetch failed!
    pause
    exit /b 1
)

echo.
echo [Step 2/2] Building indexes...
python build_experimental_indexes.py
if %errorlevel% neq 0 (
    echo ERROR: Index build failed!
    pause
    exit /b 1
)

echo.
echo ===================================================
echo SUCCESS: All data updated!
echo ===================================================
echo.
echo Generated:
echo   ✓ Articles:   site_src/static/api/v2/help_center/en-us/articles/
echo   ✓ Indexes:    site_src/static/api/v2/help_center/en-us/
echo.
echo Next steps:
echo   1. Review changes: git status
echo   2. Commit: git add . && git commit -m "Update data"
echo   3. Deploy: git push origin main
echo.
pause
