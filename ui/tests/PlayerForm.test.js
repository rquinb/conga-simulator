import { localVue } from './localVueConfiguration.js'
import { mount } from '@vue/test-utils'
import PlayerForm from "../src/components/PlayerForm.vue";

describe("PlayerForm.test.js", () => {
  let wrapper;
  beforeEach(() => {
    wrapper = mount(PlayerForm, {
      localVue,
      propsData: {
        FormTitle: "Jugador 1",
        playerNum: 1
      },
      attachToDocument: true 
    });
  });

  it('Form title displays "Jugador 1"', async () => {
    expect(wrapper.find('legend').text()).toEqual('Jugador 1');
  });

  it('Form title displays "Jugador 2"', async () => {
    await wrapper.setProps({FormTitle: "Jugador 2", playerNum: 2});
    expect(wrapper.find('legend').text()).toEqual('Jugador 2');
  });

  it('Input class gets resolved as "input-player-1"', async () => {
    expect(wrapper.find('.input-player-1').exists()).toBe(true);
  });

  it('Input class gets resolved as "input-player-2"', async () => {
    await wrapper.setProps({FormTitle: "Jugador 2", playerNum: 2});
    expect(wrapper.find('.input-player-2').exists()).toBe(true);
  });

  it('No instance of class "input-player-2" gets created with current props', async () => {
    expect(wrapper.find('.input-player-2').exists()).toBe(false);
  });

  it('No instance of class "input-player-1" gets created with current props', async () => {
    await wrapper.setProps({FormTitle: "Jugador 2", playerNum: 2});
    expect(wrapper.find('.input-player-1').exists()).toBe(false);
  });

  it('Form has 3 range inputs', async () => {
    let rangeInputs = wrapper.findAll('input[type="range"]');
    expect(rangeInputs).toHaveLength(3);
  });

  it('There are 2 options for type of agent dropdown select', async () => {
    expect(wrapper.findAll('#type-of-agent-player-1 > option')).toHaveLength(2);
  });

  it('Chooses "Conservador" agent', async () => {
    const CONSERVATIVE_CHOOOSER = 'conservative_chooser';
    let typeOfAgentSelectElement = wrapper.find("#type-of-agent-player-1")
    let availableOptions = Array.apply(null, typeOfAgentSelectElement.element.options).map((option) => option.value)
    let indexOfConservativeChooser = availableOptions.indexOf(CONSERVATIVE_CHOOOSER)
    await typeOfAgentSelectElement.findAll('option').at(indexOfConservativeChooser).setSelected();
    expect(typeOfAgentSelectElement.element.value).toEqual(CONSERVATIVE_CHOOOSER);
  });

  it('Name in input gets saved in correct variable', async () => {
    const PLAYER_NAME = "Random Name"
    let namePlayer1 = wrapper.find("#name-input-player-1")
    await namePlayer1.setValue(PLAYER_NAME)
    expect(wrapper.vm.$data.player.name).toEqual(PLAYER_NAME);
  });

  it('Min card accepted gets saved in correct variable', async () => {
    const MIN_CARD_ACCEPTED = "3";
    let minCardInput = wrapper.find("#min-accepted-cards-player-1");
    await minCardInput.setValue(MIN_CARD_ACCEPTED);
    expect(wrapper.vm.$data.player.acceptedCardsRange.minCard).toEqual(MIN_CARD_ACCEPTED);
  });

  it('Max card accepted gets saved in correct variable', async () => {
    const MAX_CARD_ACCEPTED = "10";
    let maxCardInput = wrapper.find("#max-accepted-cards-player-1");
    await maxCardInput.setValue(MAX_CARD_ACCEPTED);
    expect(wrapper.vm.$data.player.acceptedCardsRange.maxCard).toEqual(MAX_CARD_ACCEPTED);
  });

  it('Max rest before cutting gets saved in correct variable', async () => {
    const MAX_REST_BEFORE_CUTTING = "9";
    let maxRestInput = wrapper.find("#max-cut-value-player-1");
    await maxRestInput.setValue(MAX_REST_BEFORE_CUTTING);
    expect(wrapper.vm.$data.player.maxRestBeforeCutting).toEqual(MAX_REST_BEFORE_CUTTING);
  });


});
