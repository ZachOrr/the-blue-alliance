/* global cast */
import React, { PropTypes } from 'react'
import Script from 'react-load-script'

export default class CastReceiver extends React.Component {
  static propTypes = {
    setLayout: PropTypes.func.isRequired,
    addWebcastAtPosition: PropTypes.func.isRequired,
  }

  constructor(props) {
    super(props);
    this.state = { castSdkLoaded: false }
  }

  render() {
    console.log("cast render")
    return (
      <div>
        <Script
          url="//www.gstatic.com/cast/sdk/libs/caf_receiver/v3/cast_receiver_framework.js"
          onCreate={this.handleScriptCreate.bind(this)}
          onError={this.handleScriptError.bind(this)}
          onLoad={this.handleScriptLoad.bind(this)}
        />
        {this.state.castSdkLoaded && <cast-media-player></cast-media-player>}
      </div>
    )
  }

  handleScriptCreate() {
    console.log("Loading chromecast receiver API...")
  }

  handleScriptError() {
    console.log("error loading chromecast receiver")
  }

  handleScriptLoad() {
    console.log("setting layout");
    this.props.setLayout(0);

    console.log("loaded chromecast receiver");
    this.setState({castSdkLoaded: true});

    const context = cast.framework.CastReceiverContext.getInstance();
    const playerManager = context.getPlayerManager();
    playerManager.addEventListener(cast.framework.events.category.REQUEST, event => console.log(event));

    /*
    // let playerElement = document.getElementsByTagName("cast-media-player")[0];
    const castDebugLogger = cast.debug.CastDebugLogger.getInstance();
    castDebugLogger.setEnabled(true);
    castDebugLogger.showDebugLogs(true);
    */

    context.start();
  }
}
