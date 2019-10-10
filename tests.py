# tests.py

from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId

sample_lipstick_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_lipstick = {
        'type': 'Matte',
        'color': 'Pink',
        'brand': 'Victoria Secret',
        'image': 'https://images-na.ssl-images-amazon.com/images/I/51KCeM7alXL._SL1013_.jpg',
        'price': '55',
        'amount': '4'
}
sample_form_data = {
    'type': sample_lipstick['type'],
    'color': sample_lipstick['color'],
    'brand': sample_lipstick['brand'],
    'image':sample_lipstick['image'],
    'price':sample_lipstick['price'],
    'amount': sample_lipstick['amount']
}

class PlaylistsTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    
    def test_index(self):
        """Test the lipstick homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Lipstick', result.data)

    def test_new(self):
        result = self.client.get('/lipsticks/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Lipstick', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    #test showing a single lipstick
    def test_show_lipstick(self, mock_find):
        
        mock_find.return_value = sample_lipstick

        result = self.client.get(f'/lipsticks/{sample_lipstick_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Victoria Secret', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_lipstick(self, mock_find):
        """Test editing a single lipstick."""
        mock_find.return_value = sample_lipstick

        result = self.client.get(f'/lipsticks/{sample_lipstick_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Pink', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_lipstick(self, mock_insert):
        """Test submitting a new lipstick."""
        result = self.client.post('/lipsticks', data=sample_form_data)

        # After submitting, should redirect to that lipstick's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_lipstick)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_lipstick(self, mock_update):
        result = self.client.post(f'/lipsticks/{sample_lipstick_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_lipstick_id}, {'$set': sample_lipstick})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_lipstick(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/lipsticks/{sample_lipstick_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_lipstick_id})

if __name__ == '__main__':
    unittest_main()

