// import 'babel-polyfill'
import React from 'react'
// import ReactGA from 'react-ga'
import { Provider } from 'react-redux'
import thunk from 'redux-thunk'
import { createStore, applyMiddleware, compose } from 'redux'
import ReactDOM from 'react-dom'
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider'
import { indigo500, indigo700 } from 'material-ui/styles/colors'
import getMuiTheme from 'material-ui/styles/getMuiTheme'
import GamedayCastFrame from './components/GamedayCastFrame'
import gamedayReducer, { firedux } from '../gameday2/reducers'

import { setWebcastsRaw, setLayout, addWebcastAtPosition, setTwitchChat, setDefaultTwitchChat, setChatSidebarVisibility, setFavoriteTeams, togglePositionLivescore } from '../gameday2/actions'
// import { MAX_SUPPORTED_VIEWS } from './constants/LayoutConstants'
//
// ReactGA.initialize('UA-1090782-9')
//
// // const webcastData = JSON.parse(document.getElementById('webcasts_json').innerHTML)
// // const defaultChat = document.getElementById('default_chat').innerHTML

const store = createStore(gamedayReducer, compose(
  applyMiddleware(thunk),
))
firedux.dispatch = store.dispatch

const muiTheme = getMuiTheme({
  palette: {
    primary1Color: indigo500,
    primary2Color: indigo700,
  },
  layout: {
    appBarHeight: 36,
    socialPanelWidth: 300,
    chatPanelWidth: 300,
  },
})

ReactDOM.render(
  <MuiThemeProvider muiTheme={muiTheme}>
    <Provider store={store}>
      <GamedayCastFrame />
    </Provider>
  </MuiThemeProvider>,
  document.getElementById('content')
)
