
// BROSKI HYPERSAW PORTAL - One Page React App
// All users see the front page, but you get secret access to ChaosGenius Hub
// Password-protected admin zone + hidden subpages (easter egg style)

import { motion } from 'framer-motion';
import { useState } from 'react';

export default function BROskiPortal() {
  const [isAdmin, setIsAdmin] = useState(false);
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = () => {
    if (password === "chaosgeniusultra") {
      setIsAdmin(true);
    } else {
      setError("Invalid password, bro!");
    }
  };

  return (
    <div className="min-h-screen bg-black text-white p-4 space-y-10">
      <motion.h1 initial={{ opacity: 0, y: -30 }} animate={{ opacity: 1, y: 0 }} className="text-4xl text-center font-bold">
        🧠 BROSKI POWER-UP PORTAL
      </motion.h1>

      <section className="grid md:grid-cols-2 gap-6">
        <div className="bg-gray-800 p-6 rounded-xl border border-purple-500">
          <h2 className="text-xl font-bold mb-2">📝 PromptMaker Pro</h2>
          <p className="text-gray-300 mb-4">Pre-made & remixable AI prompts for hustle, chill, creativity, and madness.</p>
          <button className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg transition-all">Generate a Prompt</button>
        </div>

        <div className="bg-gray-800 p-6 rounded-xl border border-blue-500">
          <h2 className="text-xl font-bold mb-2">🎮 BossGear Loadout</h2>
          <p className="text-gray-300 mb-4">Links to top tools, ADHD modes, soundboards, and creative boosters.</p>
          <button className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-all">Open Loadout</button>
        </div>

        <div className="bg-gray-800 p-6 rounded-xl border border-pink-500">
          <h2 className="text-xl font-bold mb-2">🪩 Style Station</h2>
          <p className="text-gray-300 mb-4">Pick your BROski avatar, get an AI PFP, and activate your Flex Badge.</p>
          <button className="bg-pink-600 hover:bg-pink-700 px-4 py-2 rounded-lg transition-all">Style Me!</button>
        </div>

        <div className="bg-gray-800 p-6 rounded-xl border border-green-500">
          <h2 className="text-xl font-bold mb-2">☕ Daily Energy Boost</h2>
          <p className="text-gray-300 mb-4">Get your hype quote, BROski tip, and random boost on every refresh.</p>
          <button className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg transition-all">Get Boosted</button>
        </div>
      </section>

      {/* 🔐 Secret Admin Zone - Password Protected */}
      <section className="mt-10 text-center">
        {!isAdmin ? (
          <div className="space-y-4">
            <h2 className="text-2xl">🔒 ChaosGenius Admin Access</h2>
            <input
              placeholder="Enter password, bro..."
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              type="password"
              className="w-full max-w-xs mx-auto bg-gray-800 border border-gray-600 rounded-lg px-4 py-2 text-white"
            />
            <button
              onClick={handleLogin}
              className="bg-purple-600 hover:bg-purple-700 px-6 py-2 rounded-lg transition-all"
            >
              Unlock HUB
            </button>
            {error && <p className="text-red-500">{error}</p>}
          </div>
        ) : (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="admin-zone chaos-glow p-8 rounded-xl mt-6"
          >
            <motion.h2
              className="text-4xl font-bold mb-6 chaos-gradient bg-clip-text text-transparent"
              animate={{ y: [0, -5, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              💥 CHAOSGENIUS HUB ACTIVATED 💥
            </motion.h2>

            <div className="grid md:grid-cols-3 gap-4 mt-8">
              <motion.div
                className="bg-purple-700 p-4 rounded-lg border border-purple-400 hover:bg-purple-600 transition-all cursor-pointer"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <h3 className="font-bold text-lg">🚀 Ultra Drops</h3>
                <p className="text-sm text-purple-200">Deploy instant rewards</p>
              </motion.div>

              <motion.div
                className="bg-blue-700 p-4 rounded-lg border border-blue-400 hover:bg-blue-600 transition-all cursor-pointer"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <h3 className="font-bold text-lg">💰 BROski$ Flow</h3>
                <p className="text-sm text-blue-200">Monitor token economy</p>
              </motion.div>

              <motion.div
                className="bg-pink-700 p-4 rounded-lg border border-pink-400 hover:bg-pink-600 transition-all cursor-pointer"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <h3 className="font-bold text-lg">🎁 NFT Vault</h3>
                <p className="text-sm text-pink-200">Manage prizes & store</p>
              </motion.div>

              <motion.div
                className="bg-green-700 p-4 rounded-lg border border-green-400 hover:bg-green-600 transition-all cursor-pointer"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <h3 className="font-bold text-lg">🏆 Clan Intel</h3>
                <p className="text-sm text-green-200">Watch progress data</p>
              </motion.div>

              <motion.div
                className="bg-orange-700 p-4 rounded-lg border border-orange-400 hover:bg-orange-600 transition-all cursor-pointer"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <h3 className="font-bold text-lg">🤖 AI Engine</h3>
                <p className="text-sm text-orange-200">System diagnostics</p>
              </motion.div>

              <motion.div
                className="bg-red-700 p-4 rounded-lg border border-red-400 hover:bg-red-600 transition-all cursor-pointer"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <h3 className="font-bold text-lg">⚡ Chaos Mode</h3>
                <p className="text-sm text-red-200">Emergency override</p>
              </motion.div>
            </div>

            <motion.div
              className="mt-8 p-4 bg-black bg-opacity-50 rounded-lg border border-gray-600"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              <h4 className="text-lg font-bold mb-2">🔧 SYSTEM STATUS</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div className="text-green-400">🟢 AI Squad: ONLINE</div>
                <div className="text-green-400">🟢 Token Flow: ACTIVE</div>
                <div className="text-yellow-400">🟡 Portal: OPTIMIZING</div>
                <div className="text-green-400">🟢 Chaos Engine: STABLE</div>
              </div>
            </motion.div>

            <motion.button
              className="mt-6 bg-red-600 hover:bg-red-700 px-6 py-2 rounded-lg transition-all font-bold"
              onClick={() => setIsAdmin(false)}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
            >
              🚪 Exit Hub
            </motion.button>
          </motion.div>
        )}
      </section>
    </div>
  );
}
