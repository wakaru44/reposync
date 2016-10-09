import unittest
from mock import mock,MagicMock,patch, PropertyMock
from reposync import *


class BT(unittest.TestCase):
    def setUp(self):
        pass


class test_account_processing(BT):
    def test_empty_account_raises(s):
        s.assertRaises(AssertionError, define_path,"~/wrk","")
        s.assertRaises(TypeError, define_path,"~/wrk")


class test_repo_selector(BT):
    def setUp(s):
        def do_foo(x):
            return "{0} passed".format(x)
        s.foo = do_foo

    def test_finds_github(s):
        result = get_repos("github.com/wakaru44",{"github.com":s.foo})
        s.assertEqual(result,"wakaru44 passed")

    def test_doesnt_find_githost(s):
        result = get_repos("githost.com/wakaru44",{"bananas.com":s.foo})
        s.assertEqual(result,None)

class test_github_retriever(BT):
    def setUp(s):
        pass

    @patch('requests.get')
    def test_normal_user_returns_array(s, getMock):
	data = [ {"clone_url":"one url"}, {"clone_url":"two url"}, {"clone_url":"three url"} ]
        m1 = MagicMock
        m1.json = PropertyMock(return_value=lambda: data)
        getMock = m1
        s.assertEqual( get_repos_github("foobar") , [x["clone_url"] for x in data])

    def test_emptyuser_doesnt_bother(s):
	s.assertEqual(get_repos_github(""),None)


class test_extract_repo_name(BT):
    def test_normal_url_works(s):
        url = "https://github.com/wakaru44/reposync.git"
        s.assertEqual( extract_repo_name(url) , "reposync")

class test_clone_repo(BT):
    def test_a_normal_call_is_properly_mocked(s):
        pass # fffff I don't know how to test this crap
        return True

if __name__=="__main__":
    unittest.main()
