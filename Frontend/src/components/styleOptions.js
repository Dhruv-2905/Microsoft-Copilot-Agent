import MyImage from '../Source/bot_avatar.jpg';
import UserImage from "../Source/bot_avatar_2.jpg"

const styleOptions = {
  hideUploadButton: true,
  backgroundColor: '#ECF0F7',
  avatarSize: 40,
  botAvatarBackgroundColor: undefined, // defaults to accent color
  botAvatarImage: MyImage,
  botAvatarInitials: '',
  userAvatarBackgroundColor: undefined, // defaults to accent color
  userAvatarImage: UserImage,
  userAvatarInitials: '',
  messageActivityWordBreak: 'break-word', // 'normal' || 'break-all' || 'break-word' || 'keep-all'
  hideScrollToEndButton: true,


  // Scroll behavior
  hideScrollToEndButton: undefined, // Deprecated as of 4.14.0. Use "scrollToEndButtonBehavior" instead. Remove on or after 2023-06-02.
  autoScrollSnapOnActivity: true,
  autoScrollSnapOnActivityOffset: 0,
  autoScrollSnapOnPage: true,
  autoScrollSnapOnPageOffset: 0, // TODO: Rename from "autoScrollSnapOnPageoffset".



    // Send box
    hideSendBox: false,
    hideUploadButton: false,
    hideTelephoneKeypadButton: false,
    microphoneButtonColorOnDictate: '#F33',
  

      // Visually show spoken text
  showSpokenText: false,

  spinnerAnimationBackgroundImage: undefined,
  spinnerAnimationHeight: 16,
  spinnerAnimationWidth: 16,
  spinnerAnimationPadding: 12,


//   SEND BOX
hideSendBox: false,
hideUploadButton: false,
microphoneButtonColorOnDictate: '#F33',
sendBoxBackground: 'White',
sendBoxButtonColor: undefined, // defaults to subtle
sendBoxButtonColorOnDisabled: '#CCC',
sendBoxButtonColorOnFocus: '#333',
sendBoxButtonColorOnHover: '#333',
sendBoxDisabledTextColor: undefined, // defaults to subtle
sendBoxHeight: 50,
sendBoxMaxHeight: 200,
sendBoxTextColor: 'solid 1px #000000',
sendBoxBorderBottom: 'solid 1.5px #000000',
sendBoxBorderLeft: 'solid 1px #000000',
sendBoxBorderRight: 'solid 1px #000000',
sendBoxBorderTop: 'solid 1px #000000',
sendBoxPlaceholderColor: undefined, // defaults to subtle
sendBoxTextWrap: true,







};




export default styleOptions;
