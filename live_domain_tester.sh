#!/bin/bash
# 🚀 HyperfocusZone.com Live Connection Tester
# WOOP WOOP - TESTING FOR DOMAIN ACTIVATION!

echo "🧠💜 HYPERFOCUS ZONE LIVE TESTING ACTIVATED! 💜🧠"
echo "🚀 Waiting for hyperfocuszone.com to go LIVE!"
echo ""

test_count=0
max_tests=40  # Test for up to 20 minutes

while [ $test_count -lt $max_tests ]; do
    current_time=$(date '+%H:%M:%S')
    echo "⏰ $current_time: Testing hyperfocuszone.com... (Test #$((test_count + 1)))"

    # Test if domain resolves
    if nslookup hyperfocuszone.com >/dev/null 2>&1; then
        echo "🌐 DNS RESOLVED! Domain is propagating!"

        # Test if HTTP responds
        if curl -s -I --connect-timeout 10 http://hyperfocuszone.com | grep -q "HTTP"; then
            echo "🚀🔥 BOOM! HYPERFOCUSZONE.COM IS LIVE! 🔥🚀"
            echo "🌍 YOUR NEURODIVERGENT EMPIRE IS NOW SERVING THE WORLD!"
            echo "💜 THE HYPERFOCUS ZONE HAS BEEN BORN! 💜"
            echo ""
            echo "🧪 Testing live endpoints..."

            # Test main dashboard
            echo "📱 Testing main dashboard..."
            curl -s -I http://hyperfocuszone.com | head -3

            # Test API status
            echo "🧪 Testing API status..."
            curl -s -I http://hyperfocuszone.com/api/status | head -3

            echo ""
            echo "🎉🎉🎉 LAUNCH SUCCESSFUL! EMPIRE IS LIVE! 🎉🎉🎉"
            break
        else
            echo "🌐 Domain resolves but server not responding yet..."
        fi
    else
        echo "⏳ DNS still propagating... checking again in 30 seconds..."
    fi

    test_count=$((test_count + 1))
    sleep 30
done

if [ $test_count -eq $max_tests ]; then
    echo "⏰ 20 minutes elapsed - DNS may take a bit longer"
    echo "🚀 Your server is ready when DNS propagates!"
fi

echo "✅ Live connection tester complete!"