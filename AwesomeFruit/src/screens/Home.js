import React from 'react';
import { StyleSheet, Text, View, Button } from 'react-native';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isRequested: false,
      spoiledText: "Spoiled!",
      notSpoiledText: "Not spoiled!",
      isSpoiled: false
    };

    this.sendInformation = this.sendInformation.bind(this);
  }

  render() {
    return (
      <View style={styles.container}>
        <Text>Awesome Fruit</Text>
        <Button
          onPress={this.sendInformation}
          title="Learn More"
          color="#841584"
          accessibilityLabel="Learn more about this purple button"
        />
        <Text>{this.state.isRequested ? (this.state.isSpoiled ? this.state.spoiledText : this.state.notSpoiledText) : ""}</Text>
      </View>
    );
  }

  sendInformation() {
    //Do URL call here...

    this.setState(previousState => ({
      isRequested: true,
      spoiledText: "Spoiled!",
      notSpoiledText: "Not spoiled!",
      isSpoiled: !previousState.isSpoiled
    }));
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
