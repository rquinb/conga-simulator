import { localVue } from './localVueConfiguration.js'
import { shallowMount } from '@vue/test-utils'
import { STATISTICS_EXAMPLE } from './statisticsMock.js'
import Statistics from "../src/components/Statistics/Statistics.vue";

describe("Statistics.test.js", () => {
    let wrapper;
    beforeEach(() => {
      wrapper = shallowMount(Statistics, {
        localVue,
        propsData: {statistics: STATISTICS_EXAMPLE}
        })
    });
    it('Display player 1 name', async () => {
        expect(wrapper.find('.name-player-1').text()).toEqual(STATISTICS_EXAMPLE.name_player_1);
        });

    it('Display player 2 name', async () => {
        expect(wrapper.find('.name-player-2').text()).toEqual(STATISTICS_EXAMPLE.name_player_2);
        });

    it('Display number of games', async () => {
        expect(wrapper.find('.number-of-games').text()).toEqual(STATISTICS_EXAMPLE.number_of_games.toString());
        });

    it('Display chart of winners proportion', async () => {
        expect(wrapper.find('.winners-proportion').exists()).toBe(true);
        });
    
    it('Display chart of rounds-histogram', async () => {
        expect(wrapper.find('.rounds-histogram').exists()).toBe(true);
        });

    it('Display chart of rounds details', async () => {
        expect(wrapper.find('.rounds-details').exists()).toBe(true);
        });

    it('Display chart of cuts comparisson', async () => {
        expect(wrapper.find('.cuts-comparison').exists()).toBe(true);
        });

    it('Display chart of cuts report for player 1', async () => {
        expect(wrapper.find('.cuts-report-player-1').exists()).toBe(true);
        });
    
    it('Display chart of cuts report for player 2', async () => {
        expect(wrapper.find('.cuts-report-player-2').exists()).toBe(true);
        });

});