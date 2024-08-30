import React, { Component } from 'react';
import Router from 'next/router';
import { Mutation } from 'react-apollo';
import gql from 'graphql-tag';
import Form from '../styles/Form';
import Error from '../ErrorMessage';
import { ALL_POLITICIANS_QUERY } from './Politicians';

const CREATE_POLITICIAN_MUTATION = gql`
	mutation CREATE_POLITICIAN_MUTATION(
		$party: String
		$name: String!
		$title: String
		$chamber: String
		$state: String
		$district: Int
		$nthCongress: String
		$phone: String
		$gender: String
		$image: String
		$largeImage: String
		$website: String
		$govUrl: String
	) {
		createPolitician(
			party: $party
			name: $name
			title: $title
			chamber: $chamber
			state: $state
			district: $district
			nthCongress: $nthCongress
			phone: $phone
			gender: $gender
			image: $image
			largeImage: $largeImage
			website: $website
			govUrl: $govUrl
		) {
			id
		}
	}
`;

class CreatePolitician extends Component {
	state = {
		party: '',
		name: '',
		title: '',
		chamber: '',
		state: '',
		district: '0',
		nthCongress: '',
		phone: '',
		gender: '',
		image: '',
		largeImage: '',
		website: '',
		govUrl: ''
	};
	handleChange = (e) => {
		const { name, type, value } = e.target;

		const val =

				type === 'number' ? parseFloat(value) :
				value;
		this.setState({ [name]: val });
	};

	uploadFile = async (e) => {
		console.log('Uploading file...');
		const files = e.target.files;
		const data = new FormData();
		data.append('file', files[0]);
		data.append('upload_preset', 'default');

		const res = await fetch('https://api.cloudinary.com/v1_1/govtrackr/image/upload', {
			method: 'POST',
			body: data
		});
		const file = await res.json();
		console.log(file);
		this.setState({
			image: file.secure_url,
			largeImage: file.eager[0].secure_url
		});
	};

	update = (cache, payload) => {
		// deletePolitician removes listing from the SERVER
		// udate will update the cache to sync the client side
		// 1. Read the cache
		const data = cache.readQuery({ query: ALL_POLITICIANS_QUERY });
		console.log(data);

		cache.writeQuery({ query: ALL_POLITICIANS_QUERY, data });
	};

	render() {
		return (
			<Mutation mutation={CREATE_POLITICIAN_MUTATION} variables={this.state}>
				{(createPolitician, { loading, error }) => (
					<Form
						onSubmit={async (e) => {
							e.preventDefault();
							const res = await createPolitician();
							console.log(res);
							Router.push({
								pathname: '/people',
								query: { id: res.data.createPolitician.id }
							});
						}}
					>
						<Error error={error} />
						<fieldset disabled={loading} aria-busy={loading}>
							<label htmlFor="file">
								Image
								<input
									type="file"
									id="file"
									name="file"
									placeholder="Upload an image"
									onChange={this.uploadFile}
								/>
								{this.state.image && <img width="200" src={this.state.image} alt="Upload Preview" />}
							</label>

							<label htmlFor="name">
								Name
								<input
									type="text"
									id="name"
									name="name"
									placeholder="Name"
									value={this.state.name}
									onChange={this.handleChange}
								/>
							</label>

							<label htmlFor="district">
								District
								<input
									type="number"
									id="district"
									name="district"
									placeholder=""
									value={this.state.district}
									onChange={this.handleChange}
								/>
							</label>

							<label htmlFor="state">
								State
								<input
									type="text"
									id="state"
									name="state"
									placeholder="State"
									value={this.state.state}
									onChange={this.handleChange}
								/>
							</label>
							<label htmlFor="website">
								Website
								<input
									type="text"
									id="website"
									name="website"
									placeholder="Website"
									value={this.state.website}
									onChange={this.handleChange}
								/>
							</label>

							<label htmlFor="title">
								Title
								<input
									type="text"
									id="title"
									name="title"
									placeholder="Title"
									value={this.state.title}
									onChange={this.handleChange}
								/>
							</label>
							<label htmlFor="chamber">
								Chamber of Congress
								<input
									type="text"
									id="chamber"
									name="chamber"
									placeholder="Chamber"
									value={this.state.chamber}
									onChange={this.handleChange}
								/>
							</label>

							<label htmlFor="party">
								Party
								<input
									type="text"
									id="party"
									name="party"
									placeholder="Party"
									value={this.state.party}
									onChange={this.handleChange}
								/>
							</label>

							<label htmlFor="nthCongress">
								nth Congress
								<input
									type="text"
									id="nthCongress"
									name="nthCongress"
									placeholder="nth Congress"
									value={this.state.nthCongress}
									onChange={this.handleChange}
								/>
							</label>
							<label htmlFor="phone">
								Phone
								<input
									type="text"
									id="phone"
									name="phone"
									placeholder="Phone"
									value={this.state.phone}
									onChange={this.handleChange}
								/>
							</label>

							<label htmlFor="govUrl">
								Congress URL
								<input
									type="text"
									id="govUrl"
									name="govUrl"
									placeholder="congress.gov url"
									value={this.state.govUrl}
									onChange={this.handleChange}
								/>
							</label>

							<button type="submit">Submit</button>
						</fieldset>
					</Form>
				)}
			</Mutation>
		);
	}
}

export default CreatePolitician;
export { CREATE_POLITICIAN_MUTATION };
