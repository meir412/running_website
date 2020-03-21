from django.test import TestCase

from running_dashboard.models import Run


class RunModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Run.objects.create(time_sec=2400, start_time="2019-12-08T15:44:16Z", route="SRID=4326;LINESTRING (34.87368130652978 32.08947242994619, 34.87379932372701 32.09066317021829, 34.86209416358735 32.09178117940173, 34.86067795722784 32.08430934606507, 34.86045265166975 32.07836416636639, 34.86005568473533 32.07400048567857, 34.86024880378436 32.07378229617679, 34.86201906173466 32.07367320123064, 34.86236238448908 32.07382775236644, 34.86297392814433 32.08060047199196, 34.86421847312753 32.08079137359604, 34.86430430381569 32.08094591269754, 34.86457252471742 32.08098227480142, 34.86501240699545 32.08184587051064, 34.86580634086426 32.0814277093963, 34.86968481509841 32.08182314441319, 34.86979210345928 32.08191859398788, 34.87075233428623 32.08834984761884, 34.87343990771985 32.08798625524364, 34.87348282306437 32.08807260856381, 34.87348282306437 32.08807260856381, 34.87350428073619 32.08807715347327)")

    def test_time_sec_label(self):
        run = Run.objects.get(id=1)
        field_label = run._meta.get_field('time_sec').verbose_name
        self.assertEquals(field_label, 'time sec')

    def test_start_time_label(self):
        run=Run.objects.get(id=1)
        field_label = run._meta.get_field('start_time').verbose_name
        self.assertEquals(field_label, 'start time')

    def test_route_label(self):
        run=Run.objects.get(id=1)
        field_label = run._meta.get_field('route').verbose_name
        self.assertEquals(field_label, 'route')

