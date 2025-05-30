#!/usr/bin/env node
/**
 * 🧪 BROski Integration Test - JavaScript to Python API Bridge
 * Tests the connection between Discord.js bot and Python BROski AI
 */

const axios = require('axios');

console.log('🧠 BROski ClanVerse Ultra - JavaScript Integration Test');
console.log('=' * 50);

async function testBROskiIntegration() {
    const baseUrl = 'http://localhost:5000';

    try {
        // Test 1: API Status
        console.log('🔌 Testing Python API connection...');
        const statusResponse = await axios.get(`${baseUrl}/api/broski/status`);

        if (statusResponse.status === 200) {
            const data = statusResponse.data;
            console.log('✅ API Connection: SUCCESS');
            console.log(`🧠 BROski Status: ${data.status}`);
            console.log(`📊 Intelligence: ${data.system_intelligence}%`);
            console.log(`🤖 Modules Loaded: ${Object.keys(data.modules_loaded).length}`);
        }

        // Test 2: Chat Functionality
        console.log('\n💬 Testing BROski AI chat...');
        const chatData = {
            user_id: 'js_integration_test',
            message: 'Hello BROski! Testing from JavaScript Discord bot integration.',
            context: {
                platform: 'discord_js',
                test_mode: true,
                server_name: 'Integration Test Server'
            }
        };

        const chatResponse = await axios.post(`${baseUrl}/api/broski/chat`, chatData);

        if (chatResponse.status === 200) {
            const response = chatResponse.data;
            console.log('✅ Chat Response: SUCCESS');
            console.log(`🎭 Style: ${response.style}`);
            console.log(`🎯 Mood Detected: ${response.mood_detected}`);
            console.log(`⚡ Energy Level: ${response.energy_level}/100`);
            console.log(`🎪 Confidence: ${Math.round(response.confidence * 100)}%`);
            console.log(`💬 Message Preview: ${response.message.substring(0, 80)}...`);

            if (response.recommendations && response.recommendations.length > 0) {
                console.log(`💡 Top Recommendation: ${response.recommendations[0]}`);
            }
        }

        // Test 3: Hyperfocus Session
        console.log('\n🎯 Testing Hyperfocus session...');
        const hyperfocusData = {
            user_id: 'js_integration_test',
            task: 'Testing BROski Discord bot integration',
            duration: 25,
            context: { test_mode: true }
        };

        const hyperfocusResponse = await axios.post(`${baseUrl}/api/broski/hyperfocus`, hyperfocusData);

        if (hyperfocusResponse.status === 200) {
            const response = hyperfocusResponse.data;
            console.log('✅ Hyperfocus Session: SUCCESS');
            console.log(`🚀 Status: ${response.status}`);
        }

        console.log('\n🎉 JavaScript-Python Integration: FULLY OPERATIONAL!');
        console.log('🤖 BROski ClanVerse Ultra Discord bot bridge is ready!');

        return true;

    } catch (error) {
        console.error('❌ Integration test failed:', error.response?.data || error.message);
        return false;
    }
}

// Run the test
testBROskiIntegration()
    .then(success => {
        if (success) {
            console.log('\n✅ All tests passed - System ready for Discord deployment!');
            process.exit(0);
        } else {
            console.log('\n❌ Integration issues detected - Check logs above');
            process.exit(1);
        }
    })
    .catch(error => {
        console.error('❌ Test execution failed:', error);
        process.exit(1);
    });
