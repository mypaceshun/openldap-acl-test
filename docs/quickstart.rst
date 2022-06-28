Quickstart
==========

インストール手順
----------------

以下のコマンドでPyPI経由でインストールが可能です。::

  pip install openldap-acl-test

Githubより最新版をインストールする場合は以下のコマンドを実施してください。::

  pip install git+http://github.com/mypaceshun/openldap-acl-test.git

コマンド利用手順
----------------

インストール後 ``acltest`` というコマンドが追加されます。
``acltest`` コマンドを利用することでテストケース定義ファイルを読み、
適切に ``slapacl`` コマンドを呼び出し、実行結果のレポートを出力します。 ::

  # acltest -c acltest_conf.yml
  [cn=admin,dc=example,dc=com -> uid=testuser,dc=example,dc=com(manage)] ..
  [cn=replica,dc=example,dc=com -> uid=testuser,dc=example,dc=com(read)] ..
  [self -> uid=testuser,dc=example,dc=com(write)] x
  [anonymous -> uid=testuser,dc=example,dc=com(auth)] .

  ---------------------------------------------------------------------------
  SUCCESS: 5  FAILURE: 1 TESTCASES: 4

``slapacl`` はデフォルトで ``/usr/sbin/slapacl`` を参照しますが、別の場所に存在する場合は、 
``--slapacl`` オプションを利用し、直接指定してください。 ::

  # acltest -c acltest_conf.yml --slapacl ./your/directory/sbin/slapacl

テストケース定義ファイル
------------------------

``acltest`` コマンドはテストケース定義ファイルをもとに ``slapacl`` コマンドを呼び出します。
テストケース定義ファイルはYAML形式で記述します。

実際の定義ファイルの例が以下になります。 ::

  acltest:
    testcases:
      - requester: "cn=admin,dc=example,dc=com"
        target: "uid=testuser,dc=example,dc=com"
        acl: manage
        attributes: 
          - sn
          - userPassword
      - requester: "cn=replica,dc=example,dc=com"
        target: "uid=testuser,dc=example,dc=com"
        acl: read
        attributes: 
          - sn
          - userPassword
      - requester: "self"
        target: "uid=testuser,dc=example,dc=com"
        acl: write
        attributes: 
          - userPassword
      - requester: "anonymous"
        target: "uid=testuser,dc=example,dc=com"
        acl: auth
        attributes: 
          - userPassword

``acltest`` というキーの辞書内 ``testcases`` をキーに持つリストにテストケースを列挙します。

``testcases`` 内には ``requester`` と ``target`` を持つ辞書型のリストを記載します。
``acl`` は設定しない場合はデフォルトで ``read``、 
``attributes`` は指定しない場合デフォルトで ``[objectClass, cn, uid]`` となります。
