import React from "react";
import { Formik, Field } from "formik";
import { connect } from "react-redux";
import { Redirect } from "react-router-dom";

import { FieldWrapper, ErrorMessage } from "../../ui/forms";
import { createDirectory, updateDirectory } from "../../api/browser";
import { requestDirectoryAction } from "../../ducks/browser";
import { MultiTagField } from "../../ui/components/autocomplete";

import buildAPIUrl from "../../routes";

class HAVCreateFolder extends React.Component {
  state = {
    saved: false,
    redirect_target: null
  };

  componentDidMount() {
    this.props.loadData();
  }

  submit = async data => {
    const finalData = { ...data };
    finalData.tags = data.tags.map(t => t.value);
    console.log(JSON.stringify(finalData, null, 2));
    let response = await this.props.submit(finalData);
    this.setState({
      saved: true,
      redirect_target: `/hav/${response.path}/`
    });
  };

  render() {
    const { saved, redirect_target } = this.state;
    if (saved && redirect_target) {
      return <Redirect to={redirect_target} />;
    }

    const {
      header_text = "Add new folder",
      save_button_text = "Create",
      initialValues = { name: "", description: "", tags: [] },
      collection_id
    } = this.props;
    console.log("collection...", collection_id);
    return (
      <div className="content">
        <h1>{header_text}</h1>
        <Formik
          onSubmit={this.submit}
          initialValues={initialValues}
          render={props => {
            console.log(props.values);
            return (
              <>
                <FieldWrapper label="Name">
                  <Field className="input" type="text" name="name" />
                  <ErrorMessage name="name" />
                </FieldWrapper>
                <FieldWrapper label="Description">
                  <Field
                    className="textarea"
                    component="textarea"
                    name="description"
                  />
                  <ErrorMessage name="description" />
                </FieldWrapper>
                <FieldWrapper label="Tags">
                  <Field
                    component={MultiTagField}
                    className="input"
                    name="tags"
                    collection_id={collection_id}
                    value={props.values.tags}
                    onChange={value => props.setFieldValue("tags", value)}
                    onBlur={props.onBlur}
                  />
                  <ErrorMessage name="tags" />
                </FieldWrapper>
                <button type="submit" onClick={props.handleSubmit}>
                  {save_button_text}
                </button>
              </>
            );
          }}
        />
        <hr />
        <pre>{JSON.stringify(this.props, null, 2)}</pre>
      </div>
    );
  }
}

class HAVUpdateFolder extends React.Component {
  componentDidMount() {
    this.props.loadData();
  }
  render() {
    if (this.props.loading) {
      return null;
    }
    const initialValues = {
      name: this.props.data.name || "",
      description: this.props.data.description || "",
      tags: this.props.data.tags_full || []
    };
    return (
      <HAVCreateFolder
        {...this.props}
        header_text={`Update folder "${initialValues.name}"`}
        save_button_text="Save"
        initialValues={initialValues}
        loadData={() => null}
      />
    );
  }
}

const HAVFolderAdd = connect(
  (state, props) => {
    const key = buildAPIUrl(props.match.params);
    const data = state.repositories[key];
    return {
      loading: data == undefined,
      data,
      collection_id: data?.collection.id
    };
  },
  (dispatch, props) => {
    const url = buildAPIUrl(props.match.params);
    return {
      loadData: () => {
        dispatch(requestDirectoryAction(url));
      },
      submit: data => createDirectory(url, data)
    };
  }
)(HAVCreateFolder);

const HAVFolderUpdate = connect(
  (state, props) => {
    // console.log("Update Folder...");
    const key = buildAPIUrl(props.match.params);
    const data = state.repositories[key];
    return {
      loading: data == undefined,
      data,
      collection_id: data?.collection.id
    };
  },
  (dispatch, props) => {
    const url = buildAPIUrl(props.match.params);
    return {
      loadData: () => {
        dispatch(requestDirectoryAction(buildAPIUrl(props.match.params)));
      },
      submit: data => updateDirectory(url, data)
    };
  }
)(HAVUpdateFolder);

export { HAVFolderAdd, HAVFolderUpdate };