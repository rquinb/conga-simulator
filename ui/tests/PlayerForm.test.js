import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import { mount, createLocalVue } from '@vue/test-utils'
import PlayerForm from "../src/components/PlayerForm.vue";

const localVue = createLocalVue();
localVue.use(BootstrapVue);
localVue.use(IconsPlugin);

describe("PlayerForm.test.js", () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(PlayerForm, {
      localVue,
      propsData: {
        FormTitle: "Jugador 1",
        playerNum: 1
      }

    });
  });

  it('Form title displays "Jugador 1"', async () => {
    expect(wrapper.find('legend').text()).toEqual('Jugador 1');
  });

  it('Input class gets resolved as "input-player-1"', async () => {
    expect(wrapper.find('.input-player-1').exists()).toBe(true);
  });

  it('No instance of class "input-player-2" gets created with current props', async () => {
    expect(wrapper.find('.input-player-2').exists()).toBe(false);
  });

  it('Form has 3 range inputs', async () => {
    let rangeInputs = wrapper.findAll('input[type="range"]');
    expect(rangeInputs).toHaveLength(3);
  });
});
