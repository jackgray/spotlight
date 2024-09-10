import React, { Component } from 'react';
import Router from 'next/router';
import { Mutation, Query } from 'react-apollo';
import gql from 'graphql-tag';
import Form from '../styles/Form';
import Error from '../ErrorMessage';
import { SINGLE_POLITICIAN_QUERY } from './SinglePolitician';

const UPDATE_POLITICIAN_MUTATION = gql`
	mutation UPDATE_POLITICIAN_MUTATION(
		$id: ID!
		$party: String
		$name: String
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
		updatePolitician(
			id: $id
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
			party
			name
			title
			chamber
			state
			district
			nthCongress
			phone
			gender
			image
			largeImage
			website
			govUrl
		}
	}
`;

class UpdatePolitician extends Component {
	state = {};
	handleChange = (e) => {
		const { name, type, value } = e.target;

		const val =

				type === 'number' ? parseFloat(value) :
				value;
		this.setState({ [name]: val });
	};

	updatePolitician = async (e, updatePoliticianMutation) => {
		e.preventDefault();
		console.log('Updating Politician');
		console.log(this.state);
		const res = await updatePoliticianMutation({
			variables: {
				id: this.props.id,
				...this.state
			}
		});
		console.log('Updated!');
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
		console.log('Updated!');
	};

	render() {
		return (
			<Query query={SINGLE_POLITICIAN_QUERY} variables={{ id: this.props.id }}>
				{({ data, loading }) => {
					if (loading) return <p>Loading...</p>;
					if (!data.politician)
						return (
							<p>
								No politician found in database for ID
								{this.props.id}
							</p>
						);
					return (
						<Mutation mutation={UPDATE_POLITICIAN_MUTATION} variables={this.state}>
							{(updatePolitician, { loading, error }) => (
								<Form onSubmit={(e) => this.updatePolitician(e, updatePolitician)}>
									<Error error={error} />
									<fieldset disabled={loading} aria-busy={loading}>
										<label htmlFor="file">
											Image
											<input
												type="file"
												id="file"
												name="file"
												placeholder="Upload an image"
												defaultValue={data.politician.image}
												onChange={this.uploadFile}
											/>
											{this.state.image && (
												<img width="200" src={this.state.image} alt="Upload Preview" />
											)}
										</label>
										<label htmlFor="name">
											Name
											<input
												type="text"
												id="name"
												name="name"
												placeholder="Name"
												defaultValue={this.state.name}
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
												defaultValue={this.state.district}
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
												defaultValue={this.state.state}
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
												defaultValue={this.state.website}
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
												defaultValue={this.state.title}
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
												defaultValue={this.state.chamber}
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
												defaultValue={this.state.party}
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
												defaultValue={this.state.nthCongress}
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
												defaultValue={this.state.phone}
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
												defaultValue={this.state.govUrl}
												onChange={this.handleChange}
											/>
										</label>
										<button type="submit">Save Changes</button>
									</fieldset>
								</Form>
							)}
						</Mutation>
					);
				}}
			</Query>
		);
	}
}

export default UpdatePolitician;
export { UPDATE_POLITICIAN_MUTATION };
