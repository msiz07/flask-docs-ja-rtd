@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=.
set BUILDDIR=_build
if "%SPHINXINTL%" == "" (
	set SPHINXINTL=sphinx-intl
)
set LOCALEDIR=_locales

if "%1" == "" goto help
if "%1" == "gettext" goto gettext
if "%1" == "locale" goto locale
if "%1" == "trans_stat" goto trans_stat
if "%1" == "html_ja" goto html_ja
if "%1" == "rtd_ja" goto rtd_ja

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
echo.
echo This make.bat add the following targets
echo   gettext     to generate pot files (run: sphinx-build -b gettext)
echo   locale      to generate locale mo,po files (run: sphinx-intl update)
echo   trans_stat  to output translation stat (run: sphinx-intl stat)
echo   html_ja     to generate ja translated html files
echo   rtd_ja      to generate ja translated html files with rtd extensions
goto end

:gettext
%SPHINXBUILD% -b gettext %SOURCEDIR% %LOCALEDIR%\pot %SPHINXOPTS%
goto end

:locale
%SPHINXINTL% update -p %LOCALEDIR%\pot -d %LOCALEDIR% -l ja
goto end

:trans_stat
%SPHINXINTL% stat -d %LOCALEDIR% -l ja
goto end

:html_ja
%SPHINXBUILD% -M html %SOURCEDIR% %BUILDDIR% -D language=ja %SPHINXOPTS%
goto end

:rtd_ja
REM %SPHINXBUILD% -P -T -E -b readthedocs -D language=ja %SOURCEDIR% %BUILDDIR%/html
%SPHINXBUILD% -M readthedocs %SOURCEDIR% %BUILDDIR% -D language=ja %SPHINXOPTS%
goto end

:end
popd
