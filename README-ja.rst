Flaskドキュメント非公式翻訳
==================================================

軽量のWebアプリケーション用フレームワーク、Flaskのドキュメントを非公式に翻訳
しています。

この文書は「Flask Documentation」の日本語訳です。日本語訳は参考情報であって、
公式な文書ではありません。

Flask Documentation」の最新情報は https://flask.palletsprojects.com/ を参照
してください。

使い方
--------------------------------------------------

ドキュメントは `Sphinx`_ の国際化機能を使って作成します。

作成後の内容は `Read the Docs`_ を使って、以下のサイトで公開しています
（どちらのURLでもアクセスできます）。

- https://msiz07-flask-docs-ja.readthedocs.io/
- https://msiz07-flask-docs-ja.rtfd.io/

自分でビルドしたい場合は「`ビルド方法`_」を参照してください。

.. _Sphinx: https://github.com/sphinx-doc/sphinx
.. _Read the Docs: https://docs.readthedocs.io/

ビルド方法
--------------------------------------------------

Pythonバージョン
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python 3.7以上が必要です（Flaskのインストールに必要なため）。

ビルド手順
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

venvを使って仮想環境を作成してビルドする手順を以下に示します。以下のコマンド
は、Python実行ファイルは「python3」とし、Linux（bash）上でビルドする例になり
ます。

.. code-block:: sh

  $ python3 -m venv _venv
  $ source _venv/bin/activate
  $ git clone https://github.com/msiz07/flask-docs-ja-rtd.git
  $ cd flask-docs-ja-rtd
  $ git checkout 2.2.2-docs-ja
  $ git submodule init
  $ git submodule update
  $ python3 -m pip install --upgrade pip setuptools
  $ pip install --upgrade -r requirements.txt --progress-bar=off
  $ pip install --upgrade -r requirements-trans.txt --progress-bar=off
  $ invoke html-trans
  $ ls _build/html

「``_build/html``」にビルド後のファイル一式が存在すればビルド成功です。
「``_build/html/index.html``」をブラウザで表示すると、ビルドした日本語
ドキュメントのトップページを表示できます。


その他の注意事項
--------------------------------------------------

免責事項について
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

原文を正しく翻訳するよう心がけていますが、意図しない誤訳やドキュメントの不備
があるかもしれません。従って、正確性や安全性を保証するものではありません。

翻訳結果の内容によって生じた一切の責任を負いかねますので、ご了承ください。

ライセンスについて
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ドキュメントの原文は「`Flaskのライセンス`_」（BSD-3-Clause Source License）の
とおりライセンスされています。

ライセンスの中で以下の記述がある通り、ドキュメントや配布物中にあるFlaskの
copyright保持者やcontributorの名前は、（原文から派生したproductである）この
日本語訳の宣伝または販売促進（endorse or promote）に使用しているものではあり
ません。

  Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

.. _Flaskのライセンス: https://flask.palletsprojects.com/en/2.0.x/license/

プライバシーポリシーについて
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

前述の `Read the Docs`_ を使って翻訳結果を公開しているサイトでは、Googleに
よるアクセス解析ツール「Googleアナリティクス」を利用しています。

このGoogleアナリティクスはアクセス情報の収集のためにCookie（クッキー）を使用
しています。このアクセス情報は匿名で収集されており、個人を特定するものではあり
ません。

Googleアナリティクスの利用規約に関して確認したい場合は、
「`Googleアナリティクス利用規約`_」をご確認ください。

また、「ユーザーが Google パートナーのサイトやアプリを使用する際の Googleに
よるデータ使用」に関して確認したい場合は、「`Google ポリシーと規約：広告`_」
をご確認ください。

.. _Googleアナリティクス利用規約: https://www.google.com/analytics/terms/jp.html
.. _Google ポリシーと規約：広告: https://policies.google.com/technologies/partner-sites?hl=ja
