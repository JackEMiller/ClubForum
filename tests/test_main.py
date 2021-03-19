from src import main
from src.main import app
from src.models import db, Users, Classes, Techniques, Members, ClassesTechnique, ClassesMember
from flask_testing import TestCase
from flask import url_for
import datetime


class TestBase(TestCase):

    def create_app(self):
        app.config.update(SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:root@localhost/db",
                SECRET_KEY='TEST_SECRET_KEY',
                DEBUG=True,
                WTF_CSRF_ENABLED=False)
        return app

    def setUp(self):
        db.create_all()
        sampleuser = Users(user_name="test",password="test")
        db.session.add(sampleuser)
        sampletechnique = Techniques(name="test",difficulty="test",description="test")
        db.session.add(sampletechnique)
        samplemember = Members(name="test",level="test",affiliation="test")
        db.session.add(samplemember)
        date = datetime.datetime.now()
        sampleclass = Classes(date=date)
        db.session.add(sampleclass)
        db.session.commit()
        techniqueintersect = ClassesTechnique(class_id = sampleclass.id,technique_id=sampletechnique.id)
        db.session.add(techniqueintersect)
        memberintersect = ClassesMember(class_id=sampleclass.id, member_id=samplemember.id)
        db.session.add(memberintersect)
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestViews(TestBase):

    def test_home_get(self):
        response = self.client.get(url_for('app.index'))
        self.assertEqual(response.status_code, 200)

    def test_viewclass_get(self):
        response = self.client.get(url_for('app.viewclass',id=0,typeof=0))
        self.assertEqual(response.status_code, 200)

    def test_viewclass_get_1(self):
        response = self.client.get(url_for('app.viewclass',id=1,typeof=1))
        self.assertEqual(response.status_code, 200)

    def test_viewclass_get_2(self):
        response = self.client.get(url_for('app.viewclass',id=1,typeof=2))
        self.assertEqual(response.status_code, 200)

    def test_signup_get(self):
        response = self.client.get(url_for('app.signup'))
        self.assertEqual(response.status_code, 200)

    def test_view_get(self):
        response = self.client.get(url_for('app.view',error=0))
        self.assertEqual(response.status_code, 200)

    def test_updatemember_get(self):
        response = self.client.get(url_for('app.updatemember',id=1))
        self.assertEqual(response.status_code, 200)

    def test_updatetechnique_get(self):
        response = self.client.get(url_for('app.updatetechnique',id=1))
        self.assertEqual(response.status_code, 200)

    def test_addclass_get(self):
        response = self.client.get(url_for('app.addclass',studentcount=1,techniquecount=1))
        self.assertEqual(response.status_code, 200)

    def test_deleteclass(self):
        response = self.client.get(url_for('app.deleteclass',cid=1))
        self.assertEqual(response.status_code, 302)

    def test_deletemember(self):
        response = self.client.get(url_for('app.deletemember', id=1))
        self.assertEqual(response.status_code, 302)

    def test_deletetechnique(self):
        response = self.client.get(url_for('app.deletetechnique', id=1))
        self.assertEqual(response.status_code, 302)

    def test_updateclass(self):
        response = self.client.get(url_for('app.updateclass', cid=1))
        self.assertEqual(response.status_code, 200)

    def test_addupdatemember(self):
        response = self.client.get(url_for('app.addupdatemember', cid=1))
        self.assertEqual(response.status_code, 302)

    def test_addupdatetechnique(self):
        response = self.client.get(url_for('app.addupdatetechnique', cid=1))
        self.assertEqual(response.status_code, 302)

    def test_deleteupdatemember(self):
        response = self.client.get(url_for('app.deleteupdatemember', cid=1))
        self.assertEqual(response.status_code, 302)

    def test_deleteupdatetechnique(self):
        response = self.client.get(url_for('app.deleteupdatetechnique', cid=1))
        self.assertEqual(response.status_code, 302)

    def test_addclass_post(self):
        date=datetime.datetime.now()
        response = self.client.post(url_for('app.addclass',studentcount=1,techniquecount=1),
                                   data = {'1':'test',
                                           '1a':'test',
                                           'classdate':date})
        self.assertEqual(response.status_code, 302)

    def test_updateclass_post(self):
        date=datetime.datetime.now()
        response = self.client.post(url_for('app.updateclass',cid=1),
                                   data = {'1':'1',
                                           '1':'1',
                                           'classdate':date})
        self.assertEqual(response.status_code, 302)

    def test_index_post(self):
        response = self.client.post(url_for('app.index'),
                                    data= {'Username':'test',
                                    'Password':'test'})
        self.assertEqual(response.status_code, 302)

    def test_index_post_b(self):
        response = self.client.post(url_for('app.index'),
                                    data= {'Username':'',
                                    'Password':'test'})
        self.assertEqual(response.status_code, 200)

    def test_index_post_c(self):
        response = self.client.post(url_for('app.index'),
                                    data= {'Username':'test',
                                    'Password':''})
        self.assertEqual(response.status_code, 200)

    def test_signup_post(self):
        response = self.client.post(url_for('app.signup'),
                                    data= {'Username':'',
                                    'Password':'test'})
        self.assertEqual(response.status_code, 200)

    def test_signup_post_b(self):
        response = self.client.post(url_for('app.signup'),
                                    data= {'Username':'test',
                                    'Password':''})
        self.assertEqual(response.status_code, 200)

    def test_signup_post_c(self):
        response = self.client.post(url_for('app.signup'),
                                    data= {'Username':'test',
                                    'Password':'test'})
        self.assertEqual(response.status_code, 200)

    def test_signup_post_d(self):
        response = self.client.post(url_for('app.signup'),
                                    data= {'Username':'testa',
                                    'Password':'testa'})
        self.assertEqual(response.status_code, 200)

    def test_updatemember_post(self):
        response = self.client.post(url_for('app.updatemember',id=1),
                                    data= {'name':'test',
                                    'level':'test',
                                    'affiliation':'test'})
        self.assertEqual(response.status_code, 302)

    def test_updatetechnique_post(self):
        response = self.client.post(url_for('app.updatetechnique',id=1),
                                    data= {'name':'test',
                                    'difficulty':'test',
                                    'description':'test'})
        self.assertEqual(response.status_code, 302)

    def test_view_post(self):
        response = self.client.post(url_for('app.view', error=0),
                                    data= {'submitbutton':'technique',
                                           'name':'testa',
                                           'difficulty':'testa',
                                           'description':'testa'})
        self.assertEqual(response.status_code, 302)

    def test_view_postb(self):
        response = self.client.post(url_for('app.view', error=0),
                                    data= {'submitbutton':'member',
                                           'name':'testa',
                                           'level':'testa',
                                           'affiliation':'testa'})
        self.assertEqual(response.status_code, 302)

    def test_view_postc(self):
        response = self.client.post(url_for('app.view', error=0),
                                    data= {'submitbutton':'class',
                                           'studentcount':'1',
                                           'techniquecount':'1'})
        self.assertEqual(response.status_code, 302)

