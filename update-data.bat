@echo off
echo ===================================================
echo KB_Transformer Data Update Pipeline
echo ===================================================
echo.

echo [Step 1/2] Fetching data from KnowBe4 API...
echo   - Fetching categories, sections, articles
echo   - Adding source_url to all articles
echo   - Generating JSON + HTML wrappers
docker-compose run --rm transformer python data_transformer.py
if %errorlevel% neq 0 (
    echo ERROR: Data fetch failed!
    pause
    exit /b 1
)

echo.
echo [Step 2/2] Building experimental indexes...
echo   - Reading 1,004 articles
echo   - Adding image URLs from cache
echo   - Creating visual search indexes
docker-compose run --rm transformer python build_experimental_indexes.py
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
echo   ✓ Categories: site_src/static/api/v2/help_center/en-us/categories/
echo   ✓ Sections:   site_src/static/api/v2/help_center/en-us/sections/
echo   ✓ Articles:   site_src/static/api/v2/help_center/en-us/articles/ (with source_url)
echo   ✓ Enhanced:   site_src/static/api/v2/help_center/en-us/experimental/
echo.
echo Next steps:
echo   1. Review changes: git status
echo   2. Commit: git add . && git commit -m "Update data"
echo   3. Deploy: git push origin main
echo.
pause
