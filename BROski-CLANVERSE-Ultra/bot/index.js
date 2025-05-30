/**
 * 🧠 BROski ClanVerse Ultra - JavaScript Integration Bridge
 * Connects Discord.js bot with Python BROski AI Core
 */

const { Client, GatewayIntentBits, EmbedBuilder, Collection } = require('discord.js');
const { spawn } = require('child_process');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Load environment variables
require('dotenv').config({ path: '../../.env' });

// Bot configuration
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildMembers,
        GatewayIntentBits.DirectMessages
    ]
});

// Commands collection
client.commands = new Collection();

// BROski AI Bridge Configuration
const BROSKI_PYTHON_HOST = process.env.FLASK_HOST || 'localhost';
const BROSKI_PYTHON_PORT = process.env.FLASK_PORT || 3000;

class BROskiAIBridge {
    constructor() {
        this.isConnected = false;
        this.pythonProcess = null;
    }

    async connectToPythonCore() {
        try {
            // Test connection to Python BROski system
            const response = await axios.get(`http://${BROSKI_PYTHON_HOST}:${BROSKI_PYTHON_PORT}/api/health`);
            this.isConnected = response.data.status === 'healthy';
            console.log('🔗 BROski AI Bridge: Connected to Python Core!');
            return true;
        } catch (error) {
            console.log('⚠️ BROski AI Bridge: Python Core not running, starting fallback mode...');
            this.isConnected = false;
            return false;
        }
    }

    async queryBROskiAI(userId, message, context = {}) {
        if (!this.isConnected) {
            return {
                message: "🌟 BROski here! I'm running in lite mode right now, but still ready to help!",
                style: "high_energy",
                mood_detected: "neutral",
                energy_level: 85
            };
        }

        try {
            const requestData = {
                user_id: userId,
                message: message,
                context: {
                    platform: 'discord_js',
                    ...context
                }
            };

            const response = await axios.post(
                `http://${BROSKI_PYTHON_HOST}:${BROSKI_PYTHON_PORT}/api/broski/chat`,
                requestData,
                { timeout: 10000 }
            );

            return response.data;
        } catch (error) {
            console.error('Error querying BROski AI:', error.message);
            return this.getFallbackResponse();
        }
    }

    getFallbackResponse() {
        const responses = [
            "🚀 BROski here! I'm having a quick brain moment, but I'm still pumped to help!",
            "⚡ Technical difficulties can't stop the BROski energy! What's up?",
            "🔧 System's doing a quick refresh, but I'm still your productivity wingman!",
            "🌟 BROski lite mode activated! Still here to support you!"
        ];

        return {
            message: responses[Math.floor(Math.random() * responses.length)],
            style: "high_energy",
            mood_detected: "neutral",
            energy_level: 75
        };
    }
}

// Initialize BROski AI Bridge
const broskiAI = new BROskiAIBridge();

// Bot ready event
client.once('ready', async () => {
    console.log('\n🚀 BROski ClanVerse Ultra Bot ONLINE!');
    console.log(`🔗 Connected as ${client.user.tag}`);
    console.log(`🎯 Serving ${client.guilds.cache.size} server(s)`);

    // Connect to Python BROski AI
    await broskiAI.connectToPythonCore();

    // Set bot status
    client.user.setActivity('🧠 ClanVerse Ultra | !broski for AI help', { type: 'WATCHING' });

    console.log('🎉 BROski ClanVerse Ultra: FULLY OPERATIONAL!');
});

// Message handler for BROski AI interaction
client.on('messageCreate', async (message) => {
    // Ignore bot messages
    if (message.author.bot) return;

    // Check if message mentions BROski or uses command
    const content = message.content.toLowerCase();
    const isBROskiCommand = content.startsWith('!broski') ||
                           content.includes('broski') ||
                           content.startsWith('!ai');

    if (isBROskiCommand) {
        try {
            // Extract message content
            let userMessage = message.content.replace(/^!(broski|ai)\s*/i, '').trim();
            if (!userMessage && content.includes('broski')) {
                userMessage = message.content.trim();
            }

            if (!userMessage) {
                // Show help embed
                const helpEmbed = new EmbedBuilder()
                    .setColor(0x00ff88)
                    .setTitle('🧠 BROski ClanVerse Ultra AI')
                    .setDescription('Your neurodivergent productivity companion is here!')
                    .addFields(
                        {
                            name: '💬 How to Chat',
                            value: '`!broski [your message]`\nExample: `!broski I need motivation for coding`',
                            inline: false
                        },
                        {
                            name: '🎯 What I Can Help With',
                            value: '• ADHD-friendly productivity tips\n• Mood analysis & support\n• Hyperfocus guidance\n• Personalized motivation',
                            inline: false
                        },
                        {
                            name: '⚡ Quick Commands',
                            value: '• `!broski status` - System status\n• `!broski focus` - Hyperfocus session\n• `!broski mood` - Mood check',
                            inline: false
                        }
                    )
                    .setFooter({ text: 'BROski ClanVerse Ultra • Neurodivergent Excellence Engine' });

                await message.reply({ embeds: [helpEmbed] });
                return;
            }

            // Show typing indicator
            await message.channel.sendTyping();

            // Build context
            const context = {
                server_name: message.guild ? message.guild.name : 'DM',
                channel_name: message.channel.name || 'direct',
                interaction_type: 'discord_js_message'
            };

            // Query BROski AI
            const response = await broskiAI.queryBROskiAI(
                message.author.id,
                userMessage,
                context
            );

            // Create response embed
            const responseEmbed = new EmbedBuilder()
                .setColor(0x00ff88)
                .setTitle(`🧠 BROski ${response.style?.replace('_', ' ') || 'Ultra'}`)
                .setDescription(response.message)
                .setTimestamp();

            // Add additional fields if available
            if (response.mood_detected) {
                responseEmbed.addFields({
                    name: '🎭 Detected Mood',
                    value: `${response.mood_detected} ${response.confidence ? `(${Math.round(response.confidence * 100)}%)` : ''}`,
                    inline: true
                });
            }

            if (response.energy_level) {
                responseEmbed.addFields({
                    name: '⚡ Energy Level',
                    value: `${response.energy_level}/100`,
                    inline: true
                });
            }

            if (response.motivation_boost) {
                responseEmbed.addFields({
                    name: '💪 Motivation Boost',
                    value: response.motivation_boost,
                    inline: false
                });
            }

            if (response.recommendations && response.recommendations.length > 0) {
                responseEmbed.addFields({
                    name: '💡 BROski\'s Recommendation',
                    value: response.recommendations[0],
                    inline: false
                });
            }

            responseEmbed.setFooter({ text: 'BROski ClanVerse Ultra • Learning from every interaction' });

            await message.reply({ embeds: [responseEmbed] });

        } catch (error) {
            console.error('Error handling BROski interaction:', error);

            const errorEmbed = new EmbedBuilder()
                .setColor(0xff9900)
                .setTitle('🔧 BROski Brain Glitch')
                .setDescription('I\'m having a quick moment, but I\'m still here for you! Try again in a sec.')
                .setFooter({ text: 'BROski ClanVerse Ultra • Error Recovery Mode' });

            await message.reply({ embeds: [errorEmbed] });
        }
    }
});

// Slash commands setup
client.on('interactionCreate', async (interaction) => {
    if (!interaction.isChatInputCommand()) return;

    const { commandName } = interaction;

    if (commandName === 'broski') {
        const userMessage = interaction.options.getString('message');

        if (!userMessage) {
            await interaction.reply({
                content: '🧠 What would you like to chat about? Use `/broski message: your message here`',
                ephemeral: true
            });
            return;
        }

        try {
            await interaction.deferReply();

            const context = {
                server_name: interaction.guild ? interaction.guild.name : 'DM',
                channel_name: interaction.channel.name || 'direct',
                interaction_type: 'discord_js_slash'
            };

            const response = await broskiAI.queryBROskiAI(
                interaction.user.id,
                userMessage,
                context
            );

            const responseEmbed = new EmbedBuilder()
                .setColor(0x00ff88)
                .setTitle(`🧠 BROski ${response.style?.replace('_', ' ') || 'Ultra'}`)
                .setDescription(response.message)
                .setTimestamp()
                .setFooter({ text: 'BROski ClanVerse Ultra • Slash Command Response' });

            await interaction.editReply({ embeds: [responseEmbed] });

        } catch (error) {
            console.error('Error handling slash command:', error);
            await interaction.editReply({
                content: '🔧 BROski is experiencing a technical moment! Try the regular `!broski` command.',
            });
        }
    }
});

// Error handling
client.on('error', (error) => {
    console.error('🚨 Discord client error:', error);
});

process.on('unhandledRejection', (error) => {
    console.error('🚨 Unhandled promise rejection:', error);
});

// Login to Discord
const token = process.env.DISCORD_BOT_TOKEN;
if (!token) {
    console.error('🚨 ERROR: DISCORD_BOT_TOKEN not found in environment variables!');
    console.log('📝 Please add your Discord bot token to the .env file:');
    console.log('   DISCORD_BOT_TOKEN=your_token_here');
    process.exit(1);
}

client.login(token).catch((error) => {
    console.error('🚨 Failed to login to Discord:', error);
    process.exit(1);
});

module.exports = client;